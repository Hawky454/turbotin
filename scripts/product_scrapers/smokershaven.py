from . import get_html, add_item


def scrape(pbar=None):
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
        item, price, stock, link = add_item(data, name, item, price, stock, link, pbar)

    return data
