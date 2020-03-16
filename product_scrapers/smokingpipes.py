from product_scrapers.scrape_methods import get_html
from datetime import datetime
import re


def scrape():
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "smokingpipes"
    url = "https://www.smokingpipes.com/tobacco/tinned/"

    soup = get_html(url)
    for cat in soup.find_all(class_="catBox"):
        error = True
        wait_time = 2.75
        while error:
            try:
                new_soup = get_html("https://www.smokingpipes.com" + cat.find("a").get("href"))
                error = False
            except:
                print("An Error Occurred: sleeping " + str(wait_time) + "s")
                time.sleep(wait_time)
                wait_time = wait_time + 1
                pass
        for product in new_soup.find_all(class_="product"):
            for element in product.find_all():
                if element.get("class"):
                    if " ".join(element.get("class")) == "noStock":
                        if element.get_text() == "Currently Out of Stock":
                            stock = "Out of stock"
                        else:
                            stock = element.get_text().strip()
                    if " ".join(element.get("class")) == "price" and \
                            element.get_text().strip() != "Currently Out of Stock":
                        price = min(re.findall(r"\$\d+\.\d+", element.get_text().strip()))
                        stock = "In Stock"
                    if " ".join(element.get("class")) == "imgDiv":
                        for items in element.find_all("a"):
                            link = "https://www.smokingpipes.com" + items.get("href")
                if element.get("src") and not element.get("class"):
                    item = element.get("alt")
            data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                         "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
            print([name, item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
            item, price, stock, link = ["", "", "", ""]

    return data
