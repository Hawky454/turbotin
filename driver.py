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


def run_safely(func, message, log, args=None):
    try:
        start = datetime.now()
        log.write("[" + message + "] Start time: " + start.strftime("%m/%d/%Y %H:%M"))
        if args is None:
            data = func()
        else:
            data = func(*args)
        end = datetime.now()
        log.write(", End time: " + end.strftime("%m/%d/%Y %H:%M") + ", Total time: " + str(end - start) + "\n")
        return data
    except Exception as e:
        log.write(", Error time: " + datetime.now().strftime("%m/%d/%Y %H:%M") + "\n")
        log.write(str(e) + "\n")
        print()
        print(e)
        # traceback.print_exc()
        print("An error occurred while running [" + message + "]")


def scrape_products(name, pbar=None):
    module = import_module("product_scrapers." + name.replace(".py", ""))
    scrape_data = pd.DataFrame(module.scrape(pbar))
    return scrape_data


def review_data():
    data = pd.DataFrame(get_reviews("https://www.tobaccoreviews.com/browse"))
    return data


def update_website():
    # Variable allowing for relative paths
    path = os.path.dirname(__file__)

    # Initializing necessary variables
    log = open(os.path.join(path, "log.txt"), "w")
    product_data = pd.DataFrame()

    # Scrape all product data
    pbar = tqdm(os.listdir(os.path.join(path, "product_scrapers")), desc="Scraping products")
    for name in pbar:
        if name in ["__init__.py", "scrape_methods.py", "__pycache__"]:
            continue
        pbar.set_description(name[:-3])
        df = run_safely(scrape_products, name, log, [name, pbar])
        if df is not None:
            log.write(str(df.size) + " products from " + name + "\n")
        product_data = pd.concat([product_data, df])

    pickle.dump(product_data, open(os.path.join(path, "data/product_data.p"), "wb"))

    # Scrape review data
    data = run_safely(review_data, "Scraping reviews", log)
    pickle.dump(data, open(os.path.join(path, "data/review_data.p"), "wb"))

    # Categorize products
    run_safely(categorize, "Categorizing products", log, [os.path.join(path, "data/product_data.p")])

    # Load old data
    archive_data = pd.DataFrame()
    for file in tqdm(os.listdir(os.path.join(path, "archive")), desc="Loading archive"):
        df = pickle.load(open(os.path.join(path, "archive/", file), "rb"))
        archive_data = archive_data.append(df)

    # Generate the html files
    run_safely(generate_html, "Generating HTML", log, [product_data, archive_data])


if __name__ == "__main__":
    update_website()
