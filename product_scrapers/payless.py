from product_scrapers import get_html
from datetime import datetime


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "payless"
    url = "https://paylesscigarsandpipes.com/tinned-pipe-tobacco?pagesize=48&viewMode=grid&orderBy=5&pageNumber="

    next_page = True
    page_number = 1
    while next_page:
        soup = get_html(url + str(page_number))
        for product in soup.find_all("div", class_="item-box"):
            link = "https://paylesscigarsandpipes.com" + product.find("a").get("href")
            item = product.find("h2", class_="product-title").get_text()
            item = " ".join(item.split())
            price = product.find("span", class_="actual-price").get_text()
            if product.find_all("div", class_="out-of-stock"):
                stock = "Out of stock"
            else:
                stock = "In stock"

            data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                         "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
            if pbar is not None:
                pbar.set_description(", ".join([name, item]))
            item, price, stock, link = ["", "", "", ""]
        if soup.find_all("li", class_="next-page"):
            page_number += 1
        else:
            next_page = False

    return data
