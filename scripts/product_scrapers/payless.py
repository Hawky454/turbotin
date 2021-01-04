from . import get_html, add_item


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

            item, price, stock, link = add_item(data, name, item, price, stock, link, pbar)
        if soup.find_all("li", class_="next-page"):
            page_number += 1
        else:
            next_page = False

    return data
