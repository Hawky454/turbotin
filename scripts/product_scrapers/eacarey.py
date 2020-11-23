from . import get_html
from datetime import datetime


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "eacarey"
    url = "http://www.eacarey.com/other-branded-pipe-tobacco.html"

    soup = get_html(url)
    for category in soup.find_all("div", class_="fcol"):
        if category.find_all(class_="price"):
            price = category.find(class_="price").get_text()
            item = category.find(class_="name").get_text()
            link = "http://www.eacarey.com/" + category.find("a").get("href")
            data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                         "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
            if pbar is not None:
                pbar.set_description(", ".join([name, item]))
            item, price, stock, link = ["", "", "", ""]
        else:
            new_soup = get_html("http://www.eacarey.com/" + category.find("a").get("href"))
            for product in new_soup.find_all(class_="section-multi-item"):
                price = product.find(class_="price").get_text()
                item = product.find(class_="section-multi-name").get_text()
                link = "http://www.eacarey.com/" + product.find("a").get("href")
                data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                             "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                if pbar is not None:
                    pbar.set_description(", ".join([name, item]))
                item, price, stock, link = ["", "", "", ""]

    return data
