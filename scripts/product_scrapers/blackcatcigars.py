from . import get_html, add_item


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "blackcatcigars"
    url = "https://blackcatcigars.com/pages/pipe-tobacco"

    soup = get_html(url)
    for category in soup.find("div", class_="grid").find_all("a"):
        new_soup = get_html("https://blackcatcigars.com" + category.get("href"))
        if not new_soup.find(class_="grid-link__container"):
            continue
        for product in new_soup.find(class_="grid-link__container").find_all(class_="grid__item"):
            if not product or "Sorry, there are no products in this collection" in str(product):
                continue
            link = "https://blackcatcigars.com" + product.find("a").get("href")
            price = product.find("p", class_="grid-link__meta").get_text()
            price = " ".join(price.split()).replace("$ ", "$")
            item = product.find("p", class_="grid-link__title").get_text()
            item = " ".join(item.split())
            item, price, stock, link = add_item(data, name, item, price, stock, link, pbar)
    return data
