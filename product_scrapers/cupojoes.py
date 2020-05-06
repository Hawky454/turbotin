from product_scrapers import get_html
from datetime import datetime


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "cupojoes"
    url = "https://www.cupojoes.com/pipe-tobacco"

    soup = get_html(url)
    next_page = True
    while next_page:
        for product in soup.find_all("div", class_="card-body"):
            for element in product.find_all():
                if element.get("class"):
                    if " ".join(element.get("class")) == "outofstock":
                        if element.get_text().strip() == "Out of Stock":
                            stock = "Out of stock"
                        elif element.get_text().strip() == "":
                            stock = "In Stock"
                        else:
                            stock = element.get_text().strip()
                    if " ".join(element.get("class")) == "price price--withoutTax":
                        price = element.get_text()
                    if " ".join(element.get("class")) == "card-title":
                        item = element.get_text().strip()
                        for items in element.find_all("a"):
                            link = items.get("href")
            data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                         "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
            if pbar is not None:
                pbar.set_description(", ".join([name, item]))
            item, price, stock, link = ["", "", "", ""]
        if soup.find("link", rel="next"):
            soup = get_html(soup.find("link", rel="next").get("href"))
        else:
            next_page = False

    return data
