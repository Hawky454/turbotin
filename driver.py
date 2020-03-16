from product_scraper import scrape
import pickle
from review_scraper import get_reviews
from datetime import datetime
import pandas as pd
import os
from importlib import import_module


def update_website():

    log = open("log.txt", "w")
    df = pd.DataFrame()
    for name in os.listdir("product_scrapers"):
        if name.startswith("__"):
            continue
        try:
            print(name)
            start = datetime.now()
            log.write("[" + name + "] Start time: " + start.strftime("%m/%d/%Y %H:%M"))
            module = import_module("product_scrapers."+name.replace(".py", ""))
            scrape_data = pd.DataFrame(module.scrape())
            df = pd.concat([df, scrape_data])
            end = datetime.now()
            log.write(", End time: " + end.strftime("%m/%d/%Y %H:%M") + ", Total time: " + str(end - start) + "\n")
        except Exception as e:
            log.write(", Error time: " + datetime.now().strftime("%m/%d/%Y %H:%M") + "\n")
            log.write(str(e) + "\n")
            print(e)
            print("An error occurred while scraping: " + name)

    pickle.dump(df, open(r"product_data.p", "wb"))

    if False:
        start = datetime.now()
        log.write("[TR Reviews] Start time: " + start.strftime("%m/%d/%Y %H:%M"))
        review_data = get_reviews("https://www.tobaccoreviews.com/browse")
        pickle.dump(review_data, open(r"review_data.p", "wb"))
        end = datetime.now()
        log.write(", End time: " + end.strftime("%m/%d/%Y %H:%M") + ", Total time: " + str(end - start) + "\n")
