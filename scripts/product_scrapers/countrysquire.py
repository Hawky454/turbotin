from . import get_html, add_item
from bs4 import BeautifulSoup
import json


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "countrysquire"
    url = "https://www.thecountrysquireonline.com/product-category/tobacco/name-brand-favorites/"

    soup = get_html(url)
    next_page = True
    while next_page:
        for products in soup.find_all("script", type="text/template"):
            if "product-col" in products.string:
                products_soup = BeautifulSoup(json.loads(products.string), "lxml")
                for product in products_soup.find_all("li"):
                    item = product.find("h3").text
                    price = product.find("span", class_="amount").text
                    stock = "In stock"
                    if product.find("div", class_="out-of-stock"):
                        stock = "Out of stock"
                    link = product.find("a").get("href")
                    item, price, stock, link = add_item(data, name, item, price, stock, link, pbar)
        if soup.find("a", class_="next"):
            new_url = soup.find("a", class_="next").get("href")
            soup = get_html(new_url)
        else:
            next_page = False

    return data
