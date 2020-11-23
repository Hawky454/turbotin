from . import get_html
from datetime import datetime


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "blackcatcigars"
    url = "https://blackcatcigars.com/pages/pipe-tobacco"

    soup = get_html(url)
    for category in soup.find("div", class_="grid").find_all("a"):
        new_soup = get_html("https://blackcatcigars.com" + category.get("href"))
        if not new_soup.find(class_="grid-link__container"):
            continue
        for product in new_soup.find(class_="grid-link__container").find_all(class_="grid__item"):
            if not product or "Sorry, there are no products in this collection" in str(product):
                continue
            link = "https://blackcatcigars.com" + product.find("a").get("href")
            price = product.find("p", class_="grid-link__meta").get_text()
            price = " ".join(price.split()).replace("$ ", "$")
            item = product.find("p", class_="grid-link__title").get_text()
            item = " ".join(item.split())
            data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                         "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
            if pbar is not None:
                pbar.set_description(", ".join([name, item]))
            item, price, stock, link = ["", "", "", ""]

    return data
