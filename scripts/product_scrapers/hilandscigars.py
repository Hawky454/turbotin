from . import get_html
from datetime import datetime
import re
import json


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "hilandscigars"
    url = "https://hilandscigars.com/product-tag/pipe-tobacco/page/0/"

    page_num = 0
    while True and page_num < 10:
        page_num += 1
        url = url.replace("/" + str(page_num - 1) + "/", "/" + str(page_num) + "/")
        try:
            soup = get_html(url)
        except:
            break
        if "Oops! That page can’t be found." in str(soup):
            break
        for product in soup.find("ul", class_="products").find_all("li"):
            main_item = product.find("h3").find("a").get_text()
            main_link = product.find("h3").find("a").get("href")
            if product.find(class_="button").get_text() == "Select options":
                new_soup = get_html(product.find(class_="button").get("href"))
                json_data = json.loads(new_soup.find("form", class_="variations_form").get("data-product_variations"))
                for sub_product in json_data:
                    for n in sub_product["attributes"]:
                        item = " ".join([main_item, sub_product["attributes"][n]])
                        break
                    if sub_product["is_in_stock"]:
                        stock = "In stock"
                    else:
                        stock = "Out of stock"
                    link = main_link
                    price = "${:.2f}".format(sub_product["display_price"])
                    data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                                 "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                    if pbar is not None:
                        pbar.set_description(", ".join([name, item]))

            else:
                if product.find_all("span", class_="stock-label"):
                    if product.find("span", class_="stock-label").get_text() == "Out of Stock":
                        stock = "Out of stock"
                    else:
                        stock = product.find("span", class_="stock-label").get_text()
                else:
                    stock = "In stock"
                item = product.find("h3").find("a").get_text()
                link = product.find("h3").find("a").get("href")
                price = product.find(class_="price").get_text()
                if re.match(r"\$\d{2}\.\d{2} \$\d{2}\.\d{2}", price):
                    price = re.findall(r"\$\d{2}\.\d{2} (\$\d{2}\.\d{2})", price)[0]
                data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                             "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                if pbar is not None:
                    pbar.set_description(", ".join([name, item]))
                item, price, stock, link = ["", "", "", ""]

    return data
