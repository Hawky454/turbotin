from product_scrapers.scrape_methods import get_html
from datetime import datetime
import time


def scrape():
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "marscigars"
    url = "http://www.marscigars.com/pipetobacco.aspx"

    soup = get_html(url)
    for bar in soup.find_all("table", class_="category-list"):
        # print(bar)
        for cat in bar.find_all("div", class_="category-list-item-head"):
            error = True
            wait_time = 2.75
            while error:
                try:
                    error = False
                    new_soup = get_html("http://www.marscigars.com" + cat.find("a").get("href"))
                    error = False
                except:
                    time.sleep(wait_time)
                    print("An Error Occurred: sleeping " + str(wait_time) + "s")
                    wait_time = wait_time + 1
                    pass
            for product in new_soup.find_all("div", class_="product-list-item"):
                for element in product.find_all():
                    if element.get("class"):
                        if " ".join(element.get("class")) == "product-list-cost-value":
                            priceraw = element.get_text().strip()
                            if len(priceraw) < 7:
                                price = priceraw
                            else:
                                head, sep, price = priceraw.partition("m ")
                        if " ".join(element.get("class")) == "product-list-options":
                            item = element.find("a").get_text().strip()
                            link = ("http://www.marscigars.com" + element.find("a").get("href"))
                        if " ".join(element.get("class")) == "product-list-control":
                            if element.find("input"):
                                stock = "In Stock"
                sub_soup = get_html(link)
                if sub_soup.find(class_="prod-detail-stock") and not stock == "In Stock":
                    stock = sub_soup.find(class_="prod-detail-stock").get_text()
                if stock == "":
                    stock = "In Stock"

                data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                             "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                item, price, stock, link = ["", "", "", ""]

    return data
