from . import get_html
from datetime import datetime
import time


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "mccranies"
    url = "http://www.mccranies.com/store/index.php?main_page=index&cPath=2_35"

    soup = get_html(url)
    for cat in soup.find_all(class_="categoryListBoxContents"):
        # print(cat)
        error = True
        wait_time = 2.75
        while error:
            try:
                new_soup = get_html(cat.find("a").get("href"))
                brand = cat.find("a").get_text().strip()
                error = False
            except:
                time.sleep(wait_time)
                print("An Error Occurred: sleeping " + str(wait_time) + "s")
                wait_time = wait_time + 1
                pass
        for product in new_soup.find_all("tr", {"class": ["productListing-even", "productListing-odd"]}):
            # print(product)
            for element in product.find_all():
                if element.find("h3", class_="itemTitle"):
                    item = (brand + " " + element.find("a").get_text())
                    link = element.find("a").get("href")
                if element.find_all()[:-1]:
                    price = element.get_text().strip()
                if element.find("img", class_="listingBuyNowButton"):
                    stock = "In Stock"
                if stock != "In Stock":
                    stock = "Out of stock"
            data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                         "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
            if pbar is not None:
                pbar.set_description(", ".join([name, item]))
            item, price, stock, link = ["", "", "", ""]

    return data
