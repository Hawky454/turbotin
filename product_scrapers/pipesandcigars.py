from product_scrapers.scrape_methods import get_html
from datetime import datetime
import json
import re
from slugify import slugify


def scrape():
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "pipesandcigars"
    url = "https://www.pipesandcigars.com/shop/packaged-tobacco/1800125/?v=5000"

    soup = get_html(url)
    for element in soup.find_all("script"):
        if element.get_text().startswith("var WTF"):
            json_data = json.loads(re.match("var WTF=({.+});", element.get_text()).group(1))
            for product in json_data["page"]["products"]:
                item = product["fullName"] + " " + product["pack"]
                price = r"$" + str(product["price"])
                stock = product["availability"]
                if stock == "Out of Stock":
                    stock = "Out of stock"
                link = "https://www.pipesandcigars.com/p/" + slugify(product["fullName"]) + "/" + \
                       str(product["id"])
                data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                             "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                item, price, stock, link = ["", "", "", ""]

    return data
