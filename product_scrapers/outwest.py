from product_scrapers import get_html
from datetime import datetime
import re


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "outwest"
    url = "http://www.outwesttobacco.com/Pipe-Tobacco.html"

    soup = get_html(url)
    for table in soup.find_all("table"):
        if "TIN PIPE TOBACCO" in str(table):
            for td in table.find_all("td"):
                if not td.find_all("a"):
                    continue
                for category in td.find_all("a"):
                    if not str(category.get("href")).startswith("Tinned"):
                        continue
                    cat_link = "http://www.outwesttobacco.com/" + category.get("href")
                    cat_title = category.get_text()
                    new_soup = get_html(cat_link)
                    for product in new_soup.find("div", id="content").find_all("tr"):
                        link = cat_link
                        item = product.find("p")
                        if not item:
                            continue
                        item = item.get_text()
                        item = " ".join([cat_title] + item.split())
                        price = product.find("input", attrs={"name": "price", "type": "hidden"})
                        if price:
                            price = "$" + price.get("value")
                            stock = "In stock"
                        else:
                            price = ""
                            stock = "Out of stock"

                        data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                                     "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                        if pbar is not None:
                            pbar.set_description(", ".join([name, item]))
                        item, price, stock, link = ["", "", "", ""]
    return data
