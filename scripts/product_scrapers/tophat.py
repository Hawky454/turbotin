from . import get_html
from datetime import datetime
import time
from tqdm import tqdm


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "tophat"
    url = "https://tophattobacco.com/pipes-and-pipe-tobacco/pipe-tobacco/"

    soup = get_html(url)
    for bar in soup.find_all("div", class_="mobile-filter-content"):
        for rebar in bar.find_all("ul", class_="category-nav-list"):
            for cat in rebar.find_all("li", class_="facet-item"):
                error = True
                wait_time = 2.75
                while error:
                    try:
                        new_soup = get_html(cat.find("a").get("href"))
                        error = False
                    except:
                        time.sleep(wait_time)
                        print("An Error Occurred: sleeping " + str(wait_time) + "s")
                        wait_time = wait_time + 1
                        pass
                for product in new_soup.find_all("div", class_="product-item-details"):
                    for element in product.find_all():
                        if element.get("class"):
                            if " ".join(element.get("class")) == "price-value-wrapper":
                                price = element.get_text().strip()
                            stock = "In Stock"
                            if " ".join(element.get("class")) == "product-item-title":
                                item = element.find("a").get_text().strip()
                                link = element.find("a").get("href")
                    sub_soup = get_html(link)
                    if sub_soup.find(class_="stock-message"):
                        stock = sub_soup.find(class_="stock-message").get_text().strip()

                    data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                                 "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                    if pbar is not None:
                        pbar.set_description(", ".join([name, item]))
                    item, price, stock, link = ["", "", "", ""]

    return data
