import pickle
from review_scraper import get_reviews
from datetime import datetime
import pandas as pd
import os
from importlib import import_module
from product_categorizer import categorize
from html_generator import generate_html
from tqdm import tqdm


def start_function(message, log):
    start = datetime.now()
    log.write("["+message+"] Start time: " + start.strftime("%m/%d/%Y %H:%M"))
    return start


def error_function(message, log, e):
    log.write(", Error time: " + datetime.now().strftime("%m/%d/%Y %H:%M") + "\n")
    log.write(str(e) + "\n")
    print(e)
    print("An error occurred while "+message)


def end_function(log, start):
    end = datetime.now()
    log.write(", End time: " + end.strftime("%m/%d/%Y %H:%M") + ", Total time: " + str(end - start) + "\n")


def update_website():

    # Initializing necessary variables
    log = open("log.txt", "w")
    df = pd.DataFrame()

    # Scrape all product data
    for name in tqdm(os.listdir("product_scrapers"), desc="Scraping products"):
        if name.startswith("__"):
            continue
        try:
            start = start_function(name, log)
            module = import_module("product_scrapers." + name.replace(".py", ""))
            scrape_data = pd.DataFrame(module.scrape())
            df = pd.concat([df, scrape_data])
            end_function(log, start)
        except Exception as e:
            error_function("scraping: "+name, log, e)

    pickle.dump(df, open(r"data/product_data.p", "wb"))

    # Scrape review data
    try:
        start = start_function("TR Reviews", log)
        review_data = pd.DataFrame(get_reviews("https://www.tobaccoreviews.com/browse"))
        pickle.dump(review_data, open(r"data/review_data.p", "wb"))
        end_function(log, start)
    except Exception as e:
        error_function("scraping reviews", log, e)

    # Categorize products
    try:
        start = start_function("Categorizing products", log)
        categorize("data/product_data.p")
        end_function(log, start)
    except Exception as e:
        error_function("categorizing products", log, e)

    # Generate the html files
    try:
        start = start_function("Creating HTML pages", log)
        df = pickle.load(open("data/product_data.p", "rb"))
        archive_data = pd.DataFrame()
        for file in tqdm(os.listdir("archive"), desc="Loading archive"):
            df = pickle.load(open("archive/" + file, "rb"))
            archive_data = archive_data.append(df)
        generate_html(df, archive_data)
        end_function(log, start)
    except Exception as e:
        error_function("creating HTML page", log, e)


