from product_scrapers.scrape_methods import get_html
from datetime import datetime


def scrape():
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "tobaccopipes"
    url = "https://www.tobaccopipes.com/pipe-tobacco/"

    soup = get_html(url)
    next_page = True
    while next_page:
        for product in soup.find_all(class_="product"):
            for element in product.find_all():
                if element.get("class"):
                    if " ".join(element.get("class")) == \
                            "button button--small card-figcaption-button add-to-cart-button":
                        if element.get_text() == "OUT OF STOCK":
                            stock = "Out of stock"
                        elif element.get_text() == "ADD TO CART":
                            stock = "In Stock"
                        else:
                            stock = element.get_text().strip()
                    if " ".join(element.get("class")) == "price price--withoutTax":
                        price = element.get_text()
                    if " ".join(element.get("class")) == "card-figure":
                        for items in element.find_all("a"):
                            link = items.get("href")
                if element.get("src"):
                    item = element.get("alt").strip()
            data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                         "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
            print([name, item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
            item, price, stock, link = ["", "", "", ""]
        if soup.find("link", rel="next"):
            soup = get_html(soup.find("link", rel="next").get("href"))
        else:
            next_page = False

    return data
