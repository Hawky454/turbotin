from product_scrapers import get_html
from datetime import datetime


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "countrysquire"
    url = "https://www.thecountrysquireonline.com/product-category/tobacco/name-brand-favorites/"

    soup = get_html(url)
    next_page = True
    while next_page:
        for product in soup.find_all("li", class_="product"):
            for element in product.find_all():
                if element.get("class"):
                    if " ".join(element.get("class")) == "woocommerce-Price-amount amount":
                        price = element.get_text().strip()
                    if " ".join(element.get("class")) == "product-category product-info":
                        item = element.find('h6').get_text().strip()
                        link = element.get("href")
                    if " ".join(element.get("class")) == "out-of-stock-button-inner":
                        if element.get_text().strip() == "Out of stock":
                            stock = element.get_text().strip()
                    if stock != "Out of stock":
                        stock = "In Stock"

            data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                         "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
            if pbar is not None:
                pbar.set_description(", ".join([name, item]))
            item, price, stock, link = ["", "", "", ""]
        if soup.find("a", class_="next"):
            new_url = soup.find("a", class_="next").get("href")
            soup = get_html(new_url)
        else:
            next_page = False

    return data
