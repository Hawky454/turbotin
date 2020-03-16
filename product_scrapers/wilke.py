from scrape_methods import get_html
from datetime import datetime


def scrape():
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "wilke"
    url = "https://www.wilkepipetobacco.com/tincellar"

    soup = get_html(url)
    for product in soup.find_all('ul', class_="_2Irj0"):
        for element in product.find_all('li'):
            if element.find("h3", class_="_2BULo"):
                item = element.find("h3", class_="_2BULo").get_text().strip()
            if element.find("a", class_="_2zTHN"):
                link = element.find("a", class_="_2zTHN").get("href")
            if element.find("span", class_="_23ArP"):
                price = element.find("span", class_="_23ArP").get_text().strip()
            if element.find("span", class_="_3DJ-f"):
                stock = element.find("span", class_="_3DJ-f").get_text().strip()
            if stock != "Out of stock":
                stock = "In Stock"

            data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                         "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
            print([name, item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
            item, price, stock, link = ["", "", "", ""]

    return data
