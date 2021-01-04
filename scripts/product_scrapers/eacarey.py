from . import get_html, add_item


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "eacarey"
    url = "http://www.eacarey.com/other-branded-pipe-tobacco.html"

    soup = get_html(url)
    for category in soup.find_all("div", class_="fcol"):
        if category.find_all(class_="price"):
            price = category.find(class_="price").get_text()
            item = category.find(class_="name").get_text()
            link = "http://www.eacarey.com/" + category.find("a").get("href")
            item, price, stock, link = add_item(data, name, item, price, stock, link, pbar)
        else:
            new_soup = get_html("http://www.eacarey.com/" + category.find("a").get("href"))
            for product in new_soup.find_all(class_="section-multi-item"):
                price = product.find(class_="price").get_text()
                item = product.find(class_="section-multi-name").get_text()
                link = "http://www.eacarey.com/" + product.find("a").get("href")
                item, price, stock, link = add_item(data, name, item, price, stock, link, pbar)

    return data
