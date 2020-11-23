from . import get_html
from datetime import datetime


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "thebriary"
    url = "http://www.thebriary.com/tobacco.html"

    soup = get_html(url)
    next_page = True
    while next_page:
        for product in soup.find_all("div", class_="product-item"):
            for element in product.find_all():
                if element.get("class"):
                    if " ".join(element.get("class")) == "price":
                        priceraw = element.get_text()
                        head, sep, price = priceraw.partition(":")
                        price = price.strip()
                    if " ".join(element.get("class")) == "status":
                        stock = element.get_text().strip()
                    if " ".join(element.get("class")) == "name":
                        item = element.get_text().strip()
                        link = ("http://www.thebriary.com/" + element.find("a").get("href"))
                if stock == "OUT OF STOCK" or stock == "Out of Stock":
                    stock = "Out of stock"

            data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                         "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
            if pbar is not None:
                pbar.set_description(", ".join([name, item]))
            item, price, stock, link = ["", "", "", ""]
        for page in soup.find_all(class_="paging"):
            if page.find("a", string="Next Page"):
                next_url = ("http://www.thebriary.com/" + page.find("a", string="Next Page").get("href"))
                soup = get_html(next_url)
            else:
                next_page = False

    return data
