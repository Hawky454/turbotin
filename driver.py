from product_scraper import scrape
import pickle
from review_scraper import get_reviews
from datetime import datetime
import pandas as pd


def update_website():
    website_list = [{"name": "cupojoes", "url": "https://www.cupojoes.com/pipe-tobacco"},
                    {"name": "smokingpipes", "url": "https://www.smokingpipes.com/tobacco/tinned/"},
                    {"name": "tobaccopipes", "url": "https://www.tobaccopipes.com/pipe-tobacco/"},
                    {"name": "niceashcigars",
                     "url": "https://www.niceashcigars.com/Pipe-Tobacco-s/1888.htm?searching=Y&sort=7&cat=1888&show=300&page=1"},
                    {"name": "ansteads",
                     "url": "https://ansteads.storebyweb.com/s/1000-1/b?ps=64&Dept=07%20Pipe%20Tobacco&pn="},
                    {"name": "pipesandcigars",
                     "url": "https://www.pipesandcigars.com/shop/packaged-tobacco/1800125/?v=5000"},
                    {"name": "4noggins", "url": "https://4noggins.com/tobacco/tinned-tobacco.html"},
                    {"name": "iwanries", "url": "https://www.iwanries.com/Import-Domestic-Tobacco-C14.cfm"},
                    {"name": "pipenook", "url": "https://www.thepipenook.com/store/c14/pipe-tobacco"},
                    {"name": "boswell", "url": "https://boswellpipes.com/brand-tobacco/"},
                    {"name": "windycitycigars",
                     "url": "https://windycitycigars.com/product-category/pipe-tobacco-buy-online/"},
                    {"name": "smokershaven", "url": "https://www.smokershaven.com/sh-tins/"},
                    {"name": "watchcitycigar", "url": "https://watchcitycigar.com/packaged-tobacco/"},
                    {"name": "kingsmoking", "url": "http://www.kingsmokingpipesandcigars.com/pipe-tobacco"},
                    {"name": "countrysquire",
                     "url": "https://www.thecountrysquireonline.com/product-category/tobacco/name-brand-favorites/"},
                    {"name": "cigarsintl", "url": "https://www.cigarsinternational.com/shop/pipe-tobacco/1800049/"},
                    {"name": "cdmcigars", "url": "https://www.cdmcigars.com/product-category/pipe-tobacco"},
                    {"name": "mccranies", "url": "http://www.mccranies.com/store/index.php?main_page=index&cPath=2_35"},
                    {"name": "thebriary", "url": "http://www.thebriary.com/tobacco.html"},
                    {"name": "tophat", "url": "https://tophattobacco.com/pipes-and-pipe-tobacco/pipe-tobacco/"},
                    {"name": "marscigars", "url": "http://www.marscigars.com/pipetobacco.aspx"},
                    {"name": "wilke", "url": "https://www.wilkepipetobacco.com/tincellar"}]

    df = pd.DataFrame()
    log = open("log.txt", "w")
    for website in website_list:

        try:
            start = datetime.now()
            log.write("[" + website["name"] + "] Start time: " + start.strftime("%m/%d/%Y %H:%M"))
            df = pd.concat([df, pd.DataFrame(scrape(name=[website["name"]], url=[website["url"]]))])
            print(df)
            pickle.dump(df, open(r"product_data.p", "wb"))
            end = datetime.now()
            log.write(", End time: " + end.strftime("%m/%d/%Y %H:%M") + ", Total time: " + str(end - start) + "\n")
        except Exception as e:
            log.write(", Error time: " + datetime.now().strftime("%m/%d/%Y %H:%M") + "\n")
            log.write(str(e) + "\n")
            print(e)
            print("An error occurred while scraping: " + website["name"])

    data = []
    for websites in website_list:
        try:
            [data.append(n) for n in pickle.load(open(r"Scrape_Data/" + websites["name"] + ".p", "rb"))]
        except:
            pass

    pickle.dump(data, open(r"Scrape_Data/data.p", "wb"))
    print(len(data))

    if True:
        start = datetime.now()
        log.write("[TR Reviews] Start time: " + start.strftime("%m/%d/%Y %H:%M"))
        review_data = get_reviews("https://www.tobaccoreviews.com/browse")
        pickle.dump(review_data, open(r"review_data.p", "wb"))
        end = datetime.now()
        log.write(", End time: " + end.strftime("%m/%d/%Y %H:%M") + ", Total time: " + str(end - start) + "\n")
