from . import get_html, add_item
import re


def scrape(pbar=None):
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
        item, price, stock, link = add_item(data, name, item, price, stock, link, pbar)

    return data
