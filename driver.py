from scripts.review_scraper import get_reviews
from datetime import datetime
import pandas as pd
import os
from importlib import import_module
from scripts.product_categorizer import categorize
from tqdm import tqdm
import traceback
from scripts.email_methods import send_log_email, send_update
from flask_app import db
from flask_app.models import Tobacco


def run_safely(func, message, args=None):
    time = datetime.now()
    try:
        if args is None:
            data = func()
        else:
            data = func(*args)
        time = datetime.now() - time
        return data, {"name": message, "time": time}
    except Exception as e:
        error = str(e)
        print()
        print(e)
        traceback.print_exc()
        print("An error occurred while running [" + message + "]")
        time = datetime.now() - time
        return None, {"name": message, "time": time, "error": error}


def scrape_products(name, pbar=None):
    module = import_module("scripts.product_scrapers." + name.replace(".py", ""))
    scrape_data = pd.DataFrame(module.scrape(pbar))
    return scrape_data


def get_review_data():
    data = pd.DataFrame(get_reviews("https://www.tobaccoreviews.com/browse"))
    return data


def df_to_sql(df):
    tobacco_list = []
    for index, data in df.iterrows():
        tobacco_list.append(Tobacco(**data))
    db.session.add_all(tobacco_list)
    db.session.commit()


def update_website():
    # Variable allowing for relative paths
    path = os.path.dirname(__file__)

    # Initializing necessary variables
    product_data = pd.DataFrame()
    log_data = pd.DataFrame(columns=["name", "time", "products", "error"])

    # Scrape all product data
    pbar = tqdm(os.listdir(os.path.join(path, "scripts/product_scrapers")), desc="Scraping products")
    for name in pbar:
        if name.startswith("__"):
            continue
        pbar.set_description(name[:-3])
        df, log = run_safely(scrape_products, name, [name, pbar])
        if df is not None:
            log["products"] = len(df.index)
        log_data = log_data.append(log, ignore_index=True)
        product_data = pd.concat([product_data, df])

    # Delete product data in case it could interfere with memory in remaining code
    product_data = product_data.reset_index(drop=True)
    product_data.to_feather(os.path.join(path, "data/product_data.feather"))
    product_data = None

    # Scrape review data and delete review_data variable
    review_data, log = run_safely(get_review_data, "Scraping reviews")
    log_data = log_data.append(log, ignore_index=True)
    review_data = review_data.reset_index(drop=True)
    review_data.to_feather(os.path.join(path, "data/review_data.feather"))
    review_data = None

    # Categorize products
    _, log = run_safely(categorize, "Categorizing products", [os.path.join(path, "data/product_data.feather")])
    log_data = log_data.append(log, ignore_index=True)

    # Clean data so that it can be added to the sql db
    product_data = pd.read_feather(os.path.join(path, "data/product_data.feather"))
    product_data = clean_for_archive(product_data)
    archive_filename = os.path.join(path, "archive/data{}.feather".format(datetime.now().strftime("_%m_%d_%Y_%H_%M")))
    product_data.to_feather(archive_filename)
    df_to_sql(product_data)

    # Concat it to the archive df
    archive = pd.read_feather(os.path.join(path, "data/archive.feather"))
    archive = pd.concat([archive, product_data])
    archive = clean_for_archive(archive)
    archive.to_feather(os.path.join(path, "data/archive.feather"))

    # Send the emil updates
    _, log = run_safely(send_update, "Sending Updates", [product_data, pd.read_sql("user", db.engine)])
    log_data = log_data.append(log, ignore_index=True)

    # Send results log as email
    run_safely(send_log_email, "Sending log", [log_data])


def clean_for_archive(df):
    df = df[df["item"] != ""]
    df = df.dropna(subset=["item", "link", "time"], how="any")
    df["time"] = pd.to_datetime(df["time"], format="%m/%d/%Y %H:%M")
    df = df.drop_duplicates(subset=["item", "link", "time"])
    df = df.reset_index(drop=True)
    return df


if __name__ == "__main__":
    update_website()
