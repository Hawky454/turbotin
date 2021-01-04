from . import get_html, add_item


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "wilke"
    url = "https://www.wilkepipetobacco.com/tincellar"

    soup = get_html(url)
    for product in soup.find_all('ul', class_="_3g8J4 _3Xnzg"):
        for element in product.find_all('li'):
            if element.find("h3", class_="_2BULo"):
                item = element.find("h3", class_="_2BULo").get_text().strip()
            if element.find("a", class_="_2zTHN"):
                link = element.find("a", class_="_2zTHN").get("href")
            if element.find("span", class_="_23ArP"):
                price = element.find("span", class_="_23ArP").get_text().strip()
            if element.find("span", class_="_3DJ-f"):
                stock = element.find("span", class_="_3DJ-f").get_text().strip()
            if stock != "Out of stock":
                stock = "In Stock"

            item, price, stock, link = add_item(data, name, item, price, stock, link, pbar)

    return data
