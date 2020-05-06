import pickle
from review_scraper import get_reviews
from datetime import datetime
import pandas as pd
import os
from importlib import import_module
from product_categorizer import categorize
from html_generator import generate_html
from tqdm import tqdm
import traceback
from email_methods import send_log_email, send_update


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
    module = import_module("product_scrapers." + name.replace(".py", ""))
    scrape_data = pd.DataFrame(module.scrape(pbar))
    return scrape_data


def get_review_data():
    data = pd.DataFrame(get_reviews("https://www.tobaccoreviews.com/browse"))
    return data


def update_website():
    # Variable allowing for relative paths
    path = os.path.dirname(__file__)

    # Initializing necessary variables
    product_data = pd.DataFrame()
    log_data = pd.DataFrame(columns=["name", "time", "products", "error"])

    # Scrape all product data
    pbar = tqdm(os.listdir(os.path.join(path, "product_scrapers")), desc="Scraping products")
    for name in pbar:
        if name.startswith("__"):
            continue
        pbar.set_description(name[:-3])
        df, log = run_safely(scrape_products, name, [name, pbar])
        if df is not None:
            log["products"] = df.size
        log_data = log_data.append(log, ignore_index=True)
        product_data = pd.concat([product_data, df])
        break

    # Delete product data in case it could interfere with memory in remaining code
    with open(os.path.join(path, "data/product_data.p"), "wb") as f:
        pickle.dump(product_data, f)
    product_data = None

    # Scrape review data and delete review_data variable
    review_data, log = run_safely(get_review_data, "Scraping reviews")
    log_data = log_data.append(log, ignore_index=True)
    with open(os.path.join(path, "data/review_data.p"), "wb") as f:
        pickle.dump(review_data, f)
    review_data = None

    # Categorize products
    _, log = run_safely(categorize, "Categorizing products", [os.path.join(path, "data/product_data.p")])
    log_data = log_data.append(log, ignore_index=True)
    with open(os.path.join(path, "data/product_data.p"), "rb") as f:
        product_data = pickle.load(f)
    with open(os.path.join(path, "archive/", "data" + datetime.now().strftime("_%m_%d_%Y_%H_%M") + ".p"), "wb") as f:
        if "error" not in log:
            pickle.dump(product_data, f)
    product_data = None

    # Load old data
    archive_data = pd.DataFrame()
    for file in tqdm(os.listdir(os.path.join(path, "archive")), desc="Loading archive"):
        with open(os.path.join(path, "archive/", file), "rb") as f:
            df = pickle.load(f)
        df = clean_archive_data(df)
        archive_data = archive_data.append(df)
    archive_data = archive_data.drop_duplicates()

    # Reload product data in case archive causes memory errors
    with open(os.path.join(path, "data/product_data.p"), "rb") as f:
        product_data = pickle.load(f)

    # Generate the html files
    _, log = run_safely(generate_html, "Generating HTML", [product_data, archive_data, path])
    log_data = log_data.append(log, ignore_index=True)

    # Send the emil updates
    _, log = run_safely(send_update, "Sending Updates")
    log_data = log_data.append(log, ignore_index=True)

    # Send results log as email
    run_safely(send_log_email, "Sending log", [log_data])


def clean_archive_data(df):
    df["date"] = df["time"].str.replace(r'(\d{2})\/(\d{2})\/(\d{4}).+', r'\3, \1, \2')
    df = df[df["price"].str.contains(r"^\$\d{1,3}\.\d\d$")]
    df = df[df.price != ""]
    df = df[["date", "store", "price", "brand", "blend", "stock"]]
    df["price"] = df["price"].str[1:]
    return df


if __name__ == "__main__":
    update_website()
