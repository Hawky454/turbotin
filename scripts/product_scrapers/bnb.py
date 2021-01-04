from . import get_html, add_item


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "bnb"
    url = "https://www.bnbtobacco.com/collections/tin-can-pipe-tobacco?page="

    page_number = 1
    while True:
        soup = get_html(url + str(page_number))
        if not soup.find_all("div", class_="product-grid-item"):
            break
        for product in soup.find_all("div", class_="product-grid-item"):
            link = "https://www.bnbtobacco.com" + product.find("h4").find("a").get("href")
            item = product.find("h4").get_text()
            item = " ".join(item.split())
            price = product.find("div", class_="price").get_text()
            if product.find_all("span", class_="badge badge--sold-out"):
                stock = "Out of stock"
            else:
                stock = "In stock"
            item, price, stock, link = add_item(data, name, item, price, stock, link, pbar)
        page_number += 1
    return data
