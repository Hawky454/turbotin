from product_scrapers.scrape_methods import get_html
from datetime import datetime


def scrape():
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "cdmcigars"
    url = "https://www.cdmcigars.com/product-category/pipe-tobacco"

    soup = get_html(url)
    next_page = True
    while next_page:
        for product in soup.find_all("div", class_="product"):
            for element in product.find_all():
                if element.get("class"):
                    if " ".join(element.get("class")) == "price":
                        if element.find("ins"):
                            price = element.find("ins").get_text().strip()
                        else:
                            price = element.get_text().strip()
                    if " ".join(element.get("class")) == "name product-title":
                        item = element.get_text().strip()
                        link = element.find("a").get("href")
                    if " ".join(element.get('class')) == "out-of-stock-label":
                        stock = "Out of stock"
                    if stock != "Out of stock":
                        stock = "In Stock"
            data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                         "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
            item, price, stock, link = ["", "", "", ""]
        if soup.find("a", class_="next page-number"):
            soup = get_html(soup.find("a", class_="next page-number").get("href"))
        else:
            next_page = False

    return data
