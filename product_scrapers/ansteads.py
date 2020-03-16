from scrape_methods import get_js
from datetime import datetime


def scrape():
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "ansteads"
    url = "https://ansteads.storebyweb.com/s/1000-1/b?ps=64&Dept=07%20Pipe%20Tobacco&pn="

    next_page = True
    pn = 0
    while next_page:
        pn = pn + 1
        js_soup = get_js(str(url) + str(pn))
        if "There are no results for your current search" in str(js_soup):
            next_page = False
            continue
        for product in js_soup.find_all(class_="card-content"):
            try:
                if len(product["class"]) != 1:
                    continue
                for element in product.find_all(class_="name"):
                    item = element.get_text().strip()
                    link = "https://ansteads.storebyweb.com/" + element.find("a").get("href")
                    sub_soup = get_js(link)
                    price = sub_soup.find(class_="ng-binding price-new").get_text()
                    stock = sub_soup.find("strong").get_text()
                    if stock == "Out Of Stock":
                        stock = "Out of stock"
                data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                             "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                print([name, item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
                item, price, stock, link = ["", "", "", ""]
            except:
                pass

    return data
