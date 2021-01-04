from . import get_html, add_item
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
            item, price, stock, link = add_item(data, name, item, price, stock, link, pbar)

    return data
