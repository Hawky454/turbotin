from . import get_html, add_item


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "pipeandleaf"
    url = "https://pipeandleaf.com/collections"

    soup = get_html(url)
    for category in soup.find_all("div", class_="collection-grid-item"):
        if "Pipe Tobacco" not in category.get_text():
            continue
        new_soup = get_html("https://pipeandleaf.com/" + category.find("a").get("href"))
        for product in new_soup.find_all("div", class_="product"):
            price = product.find("span", class_="product__price").get_text().replace("Regular price", "").strip()
            if product.find_all(class_="sold-out-text"):
                stock = "Out of stock"
            else:
                stock = "In stock"
            item = " ".join(product.find(class_="product__title").get_text().split())
            link = "https://pipeandleaf.com/" + product.find("a").get("href")
            item, price, stock, link = add_item(data, name, item, price, stock, link, pbar)

    return data
