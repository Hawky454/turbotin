from product_scrapers import get_html
from datetime import datetime


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "bnbtobacco"
    url = "https://www.bnbtobacco.com/collections/tin-can-pipe-tobacco?page="

    page_number = 1
    while True:
        soup = get_html(url + str(page_number))
        if not soup.find_all("div", class_="product-grid-item"):
            break
        for product in soup.find_all("div", class_="product-grid-item"):
            link = "https://www.bnbtobacco.com" + product.find("h4").find("a").get("href")
            item = product.find("h4").get_text()
            item = " ".join(item.split())
            price = product.find("div", class_="price").get_text()
            if product.find_all("span", class_="badge badge--sold-out"):
                stock = "Out of stock"
            else:
                stock = "In stock"
            data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                         "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
            if pbar is not None:
                pbar.set_description(", ".join([name, item]))
            item, price, stock, link = ["", "", "", ""]
        page_number += 1
    return data
