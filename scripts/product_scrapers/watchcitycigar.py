from . import get_html, add_item


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "watchcitycigar"
    url = "https://watchcitycigar.com/packaged-tobacco/"

    soup = get_html(url)
    next_page = True
    while next_page:
        for product in soup.find_all("li", class_="product"):
            for element in product.find_all():
                if element.get("class"):
                    if " ".join(element.get("class")) == "price-section":
                        price = element.get_text().strip()
                    if " ".join(element.get("class")) == "card-title":
                        item = element.get_text().strip()
                        link = element.find("a").get("href")
                    if " ".join(element.get("class")) == "sale-text":
                        if element.get_text().strip() == "Out of stock":
                            stock = element.get_text().strip()
                    if stock != "Out of stock":
                        stock = "In Stock"

            item, price, stock, link = add_item(data, name, item, price, stock, link, pbar)
        if soup.find("li", class_="pagination-item--next"):
            status = soup.find("li", class_="pagination-item--next")
            new_url = status.find("a", class_="pagination-link").get("href")
            soup = get_html(new_url)
        else:
            next_page = False

    return data
