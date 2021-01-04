from bs4 import BeautifulSoup
from . import get_html, add_item


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "ljperetti"
    url = "https://www.ljperetti.com/tobacco"
    soup = get_html(url)
    for li in soup.find_all("li", class_="product"):
        item = li.find("h2").text
        link = li.find("a").get("href")
        price = li.find("span").text
        stock = "In stock"
        item, price, stock, link = add_item(data, name, item, price, stock, link, pbar)

    return data
