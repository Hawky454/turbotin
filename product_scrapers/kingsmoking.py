from product_scrapers.scrape_methods import get_html
from datetime import datetime
import time


def scrape():
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "kingsmoking"
    url = "http://www.kingsmokingpipesandcigars.com/pipe-tobacco"

    soup = get_html(url)
    allinks = set()
    cats = soup.find_all("a", class_="wixAppsLink")[2:]
    for cat in cats:
        link = cat.get("href")
        if link not in allinks:
            allinks.add(link)
    for link in allinks:
        error = True
        wait_time = 2.
        while error:
            try:
                new_soup = get_html(link)
                wait_time = 2.75
                error = False
            except:
                time.sleep(wait_time)
                print("An Error Occurred: sleeping " + str(wait_time) + "s")
                wait_time = wait_time + 1
            pass
            for product in new_soup.find_all('ul', class_="_2Irj0"):
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
