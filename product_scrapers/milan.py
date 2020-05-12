from product_scrapers import get_html
from datetime import datetime
from htmlmin import minify
import re


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "milan"
    url = "https://www.milantobacco.com/pipetobacco.htm"
    soup = get_html(url)
    for category in soup.find_all("li"):
        main_link = category.find("a").get("href")
        print(main_link)
        new_soup = get_html(main_link)
        pattern = r"<(b|strong)>(.+?)</\1>.+?Size: (.+?)Availability: (.+?)Price: (.+?) USD"
        for product in re.findall(pattern, minify(str(new_soup))):
            item = product[1]
            stock = product[3].replace("<br>", "")
            if stock == "Out of Stock":
                stock = "Out of stock"
            elif stock == "In Stock":
                stock = "In stock"
            else:
                stock = ""

            price = product[4]
            link = main_link
            print([item, price, stock, link])
            data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                         "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
            if pbar is not None:
                pbar.set_description(", ".join([name, item]))
            item, price, stock, link = ["", "", "", ""]

    return data
