from . import get_html, add_item
import time


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

                    item, price, stock, link = add_item(data, name, item, price, stock, link, pbar)

    return data
