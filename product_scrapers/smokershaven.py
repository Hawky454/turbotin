from scrape_methods import get_html
from datetime import datetime


def scrape():
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "smokershaven"
    url = "https://www.smokershaven.com/sh-tins/"

    soup = get_html(url)
    for product in soup.find_all(True, {"class": ["Even wow fadeInUp", "Odd wow fadeInUp"]}):
        for element in product.find_all():
            if element.get("class"):
                if " ".join(element.get("class")) == "p-price":
                    price = element.get_text().strip()
                    if element.get_text().strip() == "":
                        stock = "Out of stock"
                    else:
                        stock = "In Stock"
                if " ".join(element.get("class")) == "pname":
                    item = element.get_text().strip()
                    link = element.get("href")
        data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                     "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
        print([name, item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
        item, price, stock, link = ["", "", "", ""]

    return data
