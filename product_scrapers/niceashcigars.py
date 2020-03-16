from scrape_methods import get_html
from datetime import datetime
import re

def scrape():
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "niceashcigars"
    url = "https://www.niceashcigars.com/Pipe-Tobacco-s/1888.htm?searching=Y&sort=7&cat=1888&show=300&page=1"

    soup = get_html(url)
    for product in soup.find_all(class_="v-product"):
        if re.search(r"Currently Backordered", product.get_text()):
            stock = "Out of stock"
        else:
            stock = "In Stock"
        for element in product.find_all():
            if element.get("class"):
                if " ".join(element.get("class")) == "product_productprice":
                    price = re.findall(r"\$\d+\.\d*", element.get_text())[0]
                if " ".join(element.get("class")) == "v-product__title productnamecolor colors_productname":
                    item = element.get_text().strip()
                    link = element.get("href")
        data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                     "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
        print([name, item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
        item, price, stock, link = ["", "", "", ""]

    return data
