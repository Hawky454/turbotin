from product_scrapers.scrape_methods import get_html
from datetime import datetime


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "windycitycigars"
    url = "https://windycitycigars.com/product-category/pipe-tobacco-buy-online/"

    soup = get_html(url)
    next_page = True
    while next_page:
        for product in soup.find_all("div", class_="box-text"):
            for element in product.find_all():
                if element.get("class"):
                    if " ".join(element.get("class")) == "price":
                        if element.find("ins"):
                            price = element.find("ins").get_text().strip()
                        else:
                            price = element.get_text().strip()
                    if " ".join(element.get("class")) == "name product-title":
                        item = element.get_text().strip()
                        link = element.find("a").get("href")
                        stock = "In Stock"
            data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                         "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
            if pbar is not None:
                pbar.set_description(", ".join([name, item]))
            item, price, stock, link = ["", "", "", ""]
        if soup.find("a", class_="next page-number"):
            soup = get_html(soup.find("a", class_="next page-number").get("href"))
        else:
            next_page = False

    return data
