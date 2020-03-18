import pickle
from review_scraper import get_reviews
from datetime import datetime
import pandas as pd
import os
from importlib import import_module
from product_categorizer import categorize
from html_generator import generate_html
from tqdm import tqdm


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
        print(e)
        print("An error occurred while running [" + message + "]")


def scrape_products(name, df):
    module = import_module("product_scrapers." + name.replace(".py", ""))
    scrape_data = pd.DataFrame(module.scrape())
    return pd.concat([df, scrape_data])


def review_data():
    pd.DataFrame(get_reviews("https://www.tobaccoreviews.com/browse"))
    pickle.dump(review_data, open(r"data/review_data.p", "wb"))


def update_website():
    # Initializing necessary variables
    log = open("log.txt", "w")
    df = pd.DataFrame()

    # Scrape all product data
    for name in tqdm(os.listdir("product_scrapers"), desc="Scraping products"):
        if name in ["__init__.py", "scrape_methods.py", "__pycache__"]:
            continue
        df = run_safely(scrape_products, name, log, [name, df])
    pickle.dump(df, open(r"data/product_data.p", "wb"))

    # Scrape review data
    run_safely(review_data, "Scraping reviews", log)

    # Categorize products
    run_safely(categorize, "Categorizing products", log, ["data/product_data.p"])

    # Generate the html files
    df = pickle.load(open("data/product_data.p", "rb"))
    archive_data = pd.DataFrame()
    for file in tqdm(os.listdir("archive"), desc="Loading archive"):
        df = pickle.load(open("archive/" + file, "rb"))
        archive_data = archive_data.append(df)
    run_safely(generate_html, "Generating HTML", log, [df, archive_data])
