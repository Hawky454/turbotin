import urllib.request as request
from bs4 import BeautifulSoup
import re
from requests_html import HTMLSession
import time
from datetime import datetime
import json
from slugify import slugify
from pyvirtualdisplay import Display
from selenium import webdriver


def get_html(url):
    req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = request.urlopen(req)
    return BeautifulSoup(response.read(), features="lxml")


def get_js(url):
    js_session = HTMLSession()
    js_response = js_session.get(url)
    js_response.html.render(timeout=16000)
    return BeautifulSoup(js_response.html.html, features="lxml")


def scrape(name, url):
    data = []

    for n in range(len(url)):

        item, price, stock, link = ["", "", "", ""]

        if name[n] == "cupojoes":
            soup = get_html(url[n])
            next_page = True
            while next_page:
                for product in soup.find_all("div", class_="card-body"):
                    for element in product.find_all():
                        if element.get("class"):
                            if " ".join(element.get("class")) == "outofstock":
                                if element.get_text().strip() == "Out of Stock":
                                    stock = "Out of stock"
                                elif element.get_text().strip() == "":
                                    stock = "In Stock"
                                else:
                                    stock = element.get_text().strip()
                            if " ".join(element.get("class")) == "price price--withoutTax":
                                price = element.get_text()
                            if " ".join(element.get("class")) == "card-title":
                                item = element.get_text().strip()
                                for items in element.find_all("a"):
                                    link = items.get("href")
                    data.append({"store": name[n], "item": item, "price": price, "stock": stock, "link": link,
                                 "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                    print([name[n], item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
                    item, price, stock, link = ["", "", "", ""]
                if soup.find("link", rel="next"):
                    soup = get_html(soup.find("link", rel="next").get("href"))
                else:
                    next_page = False

        if name[n] == "smokingpipes":
            soup = get_html(url[n])
            for cat in soup.find_all(class_="catBox"):
                error = True
                wait_time = 2.75
                while error:
                    try:
                        new_soup = get_html("https://www.smokingpipes.com" + cat.find("a").get("href"))
                        error = False
                    except:
                        print("An Error Occurred: sleeping " + str(wait_time) + "s")
                        time.sleep(wait_time)
                        wait_time = wait_time + 1
                        pass
                for product in new_soup.find_all(class_="product"):
                    for element in product.find_all():
                        if element.get("class"):
                            if " ".join(element.get("class")) == "noStock":
                                if element.get_text() == "Currently Out of Stock":
                                    stock = "Out of stock"
                                else:
                                    stock = element.get_text().strip()
                            if " ".join(element.get("class")) == "price" and \
                                    element.get_text().strip() != "Currently Out of Stock":
                                price = min(re.findall(r"\$\d+\.\d+", element.get_text().strip()))
                                stock = "In Stock"
                            if " ".join(element.get("class")) == "imgDiv":
                                for items in element.find_all("a"):
                                    link = "https://www.smokingpipes.com" + items.get("href")
                        if element.get("src") and not element.get("class"):
                            item = element.get("alt")
                    data.append({"store": name[n], "item": item, "price": price, "stock": stock, "link": link,
                                 "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                    print([name[n], item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
                    item, price, stock, link = ["", "", "", ""]

        if name[n] == "pipenook":
            soup = get_html(url[n])
            for cat in soup.find_all("a", class_="wsite-com-category-subcategory-link"):
                error = True
                wait_time = 2.75
                while error:
                    try:
                        new_soup = get_html("https://www.thepipenook.com" + cat.get("href"))
                        wait_time = 2.75
                        error = False
                    except:
                        time.sleep(wait_time)
                        print("An Error Occurred: sleeping " + str(wait_time) + "s")
                        wait_time = wait_time + 1
                    pass
                    for product in new_soup.find_all('div', class_="wsite-com-category-product-wrap"):
                        if product.find("div",
                                        class_="wsite-com-category-product-name wsite-com-link-text"):
                            item = product.find("div",
                                                class_="wsite-com-category-product-name wsite-com-link-text").get_text().strip()
                        link = "https://www.thepipenook.com" + product.find("a").get("href")
                        if product.find("div", class_="wsite-com-price"):
                            price = product.find("div", class_="wsite-com-price").get_text().strip()
                        stock = "In Stock"
                        if product.find_all("p", class_="category__out-of-stock-badge"):
                            stock = "Out of stock"

                        data.append({"store": name[n], "item": item, "price": price, "stock": stock, "link": link,
                                     "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                        print([name[n], item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
                        item, price, stock, link = ["", "", "", ""]

        if name[n] == "tobaccopipes":
            soup = get_html(url[n])
            next_page = True
            while next_page:
                for product in soup.find_all(class_="product"):
                    for element in product.find_all():
                        if element.get("class"):
                            if " ".join(element.get("class")) == \
                                    "button button--small card-figcaption-button add-to-cart-button":
                                if element.get_text() == "OUT OF STOCK":
                                    stock = "Out of stock"
                                elif element.get_text() == "ADD TO CART":
                                    stock = "In Stock"
                                else:
                                    stock = element.get_text().strip()
                            if " ".join(element.get("class")) == "price price--withoutTax":
                                price = element.get_text()
                            if " ".join(element.get("class")) == "card-figure":
                                for items in element.find_all("a"):
                                    link = items.get("href")
                        if element.get("src"):
                            item = element.get("alt").strip()
                    data.append({"store": name[n], "item": item, "price": price, "stock": stock, "link": link,
                                 "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                    print([name[n], item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
                    item, price, stock, link = ["", "", "", ""]
                if soup.find("link", rel="next"):
                    soup = get_html(soup.find("link", rel="next").get("href"))
                else:
                    next_page = False

        if name[n] == "niceashcigars":
            soup = get_html(url[n])
            for product in soup.find_all(class_="v-product"):
                if re.search(r"Currently Backordered", product.get_text()):
                    stock = "Out of stock"
                else:
                    stock = "In Stock"
                for element in product.find_all():
                    if element.get("class"):
                        if " ".join(element.get("class")) == "product_productprice":
                            price = re.findall(r"\$\d+\.\d*", element.get_text())[0]
                        if " ".join(element.get("class")) == "v-product__title productnamecolor colors_productname":
                            item = element.get_text().strip()
                            link = element.get("href")
                data.append({"store": name[n], "item": item, "price": price, "stock": stock, "link": link,
                             "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                print([name[n], item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
                item, price, stock, link = ["", "", "", ""]

        if name[n] == "ansteads":
            next_page = True
            pn = 0
            while next_page:
                pn = pn + 1
                js_soup = get_js(str(url[n]) + str(pn))
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
                        data.append({"store": name[n], "item": item, "price": price, "stock": stock, "link": link,
                                     "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                        print([name[n], item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
                        item, price, stock, link = ["", "", "", ""]
                    except:
                        pass

        if name[n] == "pipesandcigars":
            soup = get_html(url[n])
            for element in soup.find_all("script"):
                if element.get_text().startswith("var WTF"):
                    json_data = json.loads(re.match("var WTF=({.+});", element.get_text()).group(1))
                    for product in json_data["page"]["products"]:
                        item = product["fullName"] + " " + product["pack"]
                        price = r"$" + str(product["price"])
                        stock = product["availability"]
                        if stock == "Out of Stock":
                            stock = "Out of stock"
                        link = "https://www.pipesandcigars.com/p/" + slugify(product["fullName"]) + "/" + \
                               str(product["id"])
                        data.append({"store": name[n], "item": item, "price": price, "stock": stock, "link": link,
                                     "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                        print([name[n], item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
                        item, price, stock, link = ["", "", "", ""]

        if name[n] == "4noggins":
            soup = get_html(url[n])
            next_page = True
            while next_page:
                for product in soup.find_all("div", class_="product details product-item-details"):
                    for element in product.find_all():
                        if element.get("class"):
                            if " ".join(element.get("class")) == "price":
                                price = element.get_text()
                            if " ".join(element.get("class")) == "product-item-link":
                                itemraw = element.get_text().strip()
                                item = itemraw.translate({ord(":"): None})
                                link = element.get("href")
                            if " ".join(element.get("class")) == "stock unavailable":
                                stock = "Out of stock"
                        if stock != "Out of stock":
                            stock = "In Stock"

                    data.append({"store": name[n], "item": item, "price": price, "stock": stock, "link": link,
                                 "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                    print([name[n], item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
                    item, price, stock, link = ["", "", "", ""]
                if soup.find("a", class_="action next"):
                    soup = get_html(soup.find("a", class_="action next").get("href"))
                else:
                    next_page = False

        if name[n] == "iwanries":
            soup = get_html(url[n])
            for cat in soup.find_all(class_="contentCat"):
                for stuff in cat.find_all("li"):
                    # print(stuff)
                    error = True
                    wait_time = 2.75
                    while error:
                        try:
                            new_soup = get_html("https://iwanries.com/" + stuff.find("a").get("href"))
                            # print(new_soup)
                            wait_time = 2.75
                            error = False
                        except:
                            time.sleep(wait_time)
                            print("An Error Occurred: sleeping " + str(wait_time) + "s")
                            wait_time = wait_time + 1
                        pass
                    for table in new_soup.find_all('table', attrs={'align': 'center'}):
                        for product in table.find_all("td", attrs={'width': '33%'})[:-2]:
                            # print(product)
                            for element in product.find_all("a", attrs={'class': 'productName'}):
                                # print(element)
                                itemraw = element.get("title")
                                item, sep, tail = itemraw.partition(" -")
                                link = element.get("href")
                            for element in product.find_all("label", class_="productMSRP"):
                                # print(element)
                                priceraw = element.get_text()
                                head, sep, price = priceraw.partition(": ")
                            for element in product.find_all(class_="productMSRP"):
                                # print(element)
                                stockraw = element.get_text()
                                stock, sep, head = stockraw.partition(": ")
                                if stock == "Your Price":
                                    stock = "In Stock"
                                else:
                                    stock = "Out of stock"

                            data.append({"store": name[n], "item": item, "price": price, "stock": stock, "link": link,
                                         "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                            print([name[n], item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
                            item, price, stock, link = ["", "", "", ""]

        if name[n] == "windycitycigars":
            soup = get_html(url[n])
            next_page = True
            while next_page:
                for product in soup.find_all("div", class_="box-text"):
                    for element in product.find_all():
                        if element.get("class"):
                            if " ".join(element.get("class")) == "price":
                                if element.find("ins"):
                                    price = element.find("ins").get_text().strip()
                                else:
                                    price = element.get_text().strip()
                            if " ".join(element.get("class")) == "name product-title":
                                item = element.get_text().strip()
                                link = element.find("a").get("href")
                                stock = "In Stock"
                    data.append({"store": name[n], "item": item, "price": price, "stock": stock, "link": link,
                                 "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                    print([name[n], item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
                    item, price, stock, link = ["", "", "", ""]
                if soup.find("a", class_="next page-number"):
                    soup = get_html(soup.find("a", class_="next page-number").get("href"))
                else:
                    next_page = False

        if name[n] == "smokershaven":
            soup = get_html(url[n])
            for product in soup.find_all(True, {"class": ["Even wow fadeInUp", "Odd wow fadeInUp"]}):
                for element in product.find_all():
                    if element.get("class"):
                        if " ".join(element.get("class")) == "p-price":
                            price = element.get_text().strip()
                            if element.get_text().strip() == "":
                                stock = "Out of stock"
                            else:
                                stock = "In Stock"
                        if " ".join(element.get("class")) == "pname":
                            item = element.get_text().strip()
                            link = element.get("href")
                data.append({"store": name[n], "item": item, "price": price, "stock": stock, "link": link,
                             "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                print([name[n], item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
                item, price, stock, link = ["", "", "", ""]

        if name[n] == "watchcitycigar":
            soup = get_html(url[n])
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

                    data.append({"store": name[n], "item": item, "price": price, "stock": stock, "link": link,
                                 "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                    print([name[n], item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
                    item, price, stock, link = ["", "", "", ""]
                if soup.find("li", class_="pagination-item--next"):
                    status = soup.find("li", class_="pagination-item--next")
                    new_url = status.find("a", class_="pagination-link").get("href")
                    soup = get_html(new_url)
                else:
                    next_page = False

        if name[n] == "kingsmoking":
            soup = get_html(url[n])
            allinks = set()
            cats = soup.find_all("a", class_="wixAppsLink")[2:]
            for cat in cats:
                link = cat.get("href")
                if link not in allinks:
                    allinks.add(link)
            for link in allinks:
                error = True
                wait_time = 2.
                while error:
                    try:
                        new_soup = get_html(link)
                        wait_time = 2.75
                        error = False
                    except:
                        time.sleep(wait_time)
                        print("An Error Occurred: sleeping " + str(wait_time) + "s")
                        wait_time = wait_time + 1
                    pass
                    for product in new_soup.find_all('ul', class_="_2Irj0"):
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

                            data.append({"store": name[n], "item": item, "price": price, "stock": stock, "link": link,
                                         "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                            print([name[n], item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
                            item, price, stock, link = ["", "", "", ""]

        if name[n] == "countrysquire":
            soup = get_html(url[n])
            next_page = True
            while next_page:
                for product in soup.find_all("li", class_="product"):
                    for element in product.find_all():
                        if element.get("class"):
                            if " ".join(element.get("class")) == "woocommerce-Price-amount amount":
                                price = element.get_text().strip()
                            if " ".join(element.get("class")) == "product-category product-info":
                                item = element.find('h6').get_text().strip()
                                link = element.get("href")
                            if " ".join(element.get("class")) == "out-of-stock-button-inner":
                                if element.get_text().strip() == "Out of stock":
                                    stock = element.get_text().strip()
                            if stock != "Out of stock":
                                stock = "In Stock"

                    data.append({"store": name[n], "item": item, "price": price, "stock": stock, "link": link,
                                 "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                    print([name[n], item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
                    item, price, stock, link = ["", "", "", ""]
                if soup.find("a", class_="next"):
                    new_url = soup.find("a", class_="next").get("href")
                    soup = get_html(new_url)
                else:
                    next_page = False

        if name[n] == "cigarsintl":
            soup = get_html(url[n])
            next_page = True
            while next_page:
                for product in soup.find_all("div", class_="offer-prod"):
                    for element in product.find_all():
                        if element.get("class"):
                            if " ".join(element.get("class")) == "price-amount":
                                price = "$" + element.get("data-value")
                            if " ".join(element.get("class")) == "title-inner":
                                item = element.get_text().strip()
                            if " ".join(element.get("class")) == "offer-title":
                                link = ("https://www.cigarsinternational.com" + element.get("href"))
                            if " ".join(element.get("class")) == "offer-stock":
                                stock = element.get_text().strip()
                                if stock == "Out Of Stock":
                                    stock = "Out of stock"

                    data.append({"store": name[n], "item": item, "price": price, "stock": stock, "link": link,
                                 "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                    print([name[n], item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
                    item, price, stock, link = ["", "", "", ""]
                if soup.find("ul", class_="ui-pagination"):
                    status = soup.find("li", class_="ui-pagination-nav-next")
                    if status.find("span", class_="link-disabled"):
                        next_page = False
                    else:
                        new_url = "https://www.cigarsinternational.com" + status.find("a").get("href")
                        soup = get_html(new_url)

        if name[n] == "cdmcigars":
            soup = get_html(url[n])
            next_page = True
            while next_page:
                for product in soup.find_all("div", class_="product"):
                    # print(product)
                    for element in product.find_all():
                        if element.get("class"):
                            if " ".join(element.get("class")) == "price":
                                if element.find("ins"):
                                    price = element.find("ins").get_text().strip()
                                else:
                                    price = element.get_text().strip()
                            if " ".join(element.get("class")) == "name product-title":
                                item = element.get_text().strip()
                                link = element.find("a").get("href")
                            if " ".join(element.get('class')) == "out-of-stock-label":
                                stock = "Out of stock"
                            if stock != "Out of stock":
                                stock = "In Stock"
                    data.append({"store": name[n], "item": item, "price": price, "stock": stock, "link": link,
                                 "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                    print([name[n], item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
                    item, price, stock, link = ["", "", "", ""]
                if soup.find("a", class_="next page-number"):
                    soup = get_html(soup.find("a", class_="next page-number").get("href"))
                else:
                    next_page = False

        if name[n] == "mccranies":
            soup = get_html(url[n])
            for cat in soup.find_all(class_="categoryListBoxContents"):
                # print(cat)
                error = True
                wait_time = 2.75
                while error:
                    try:
                        new_soup = get_html(cat.find("a").get("href"))
                        brand = cat.find("a").get_text().strip()
                        error = False
                    except:
                        time.sleep(wait_time)
                        print("An Error Occurred: sleeping " + str(wait_time) + "s")
                        wait_time = wait_time + 1
                        pass
                for product in new_soup.find_all("tr", {"class": ["productListing-even", "productListing-odd"]}):
                    # print(product)
                    for element in product.find_all():
                        if element.find("h3", class_="itemTitle"):
                            item = (brand + " " + element.find("a").get_text())
                            link = element.find("a").get("href")
                        if element.find_all()[:-1]:
                            price = element.get_text().strip()
                        if element.find("img", class_="listingBuyNowButton"):
                            stock = "In Stock"
                        if stock != "In Stock":
                            stock = "Out of stock"
                    data.append({"store": name[n], "item": item, "price": price, "stock": stock, "link": link,
                                 "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                    print([name[n], item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
                    item, price, stock, link = ["", "", "", ""]

        if name[n] == "thebriary":
            soup = get_html(url[n])
            next_page = True
            while next_page:
                for product in soup.find_all("div", class_="product-item"):
                    for element in product.find_all():
                        if element.get("class"):
                            if " ".join(element.get("class")) == "price":
                                priceraw = element.get_text()
                                head, sep, price = priceraw.partition(":")
                                price = price.strip()
                            if " ".join(element.get("class")) == "status":
                                stock = element.get_text().strip()
                            if " ".join(element.get("class")) == "name":
                                item = element.get_text().strip()
                                link = ("http://www.thebriary.com/" + element.find("a").get("href"))
                        if stock == "OUT OF STOCK" or stock == "Out of Stock":
                            stock = "Out of stock"

                    data.append({"store": name[n], "item": item, "price": price, "stock": stock, "link": link,
                                 "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                    print([name[n], item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
                    item, price, stock, link = ["", "", "", ""]
                for page in soup.find_all(class_="paging"):
                    if page.find("a", string="Next Page"):
                        next_url = ("http://www.thebriary.com/" + page.find("a", string="Next Page").get("href"))
                        soup = get_html(next_url)
                    else:
                        next_page = False

        if name[n] == "tophat":
            soup = get_html(url[n])
            for bar in soup.find_all("div", class_="mobile-filter-content"):
                for rebar in bar.find_all("ul", class_="category-nav-list"):
                    for cat in rebar.find_all("li", class_="facet-item"):
                        error = True
                        wait_time = 2.75
                        while error:
                            try:
                                new_soup = get_html(cat.find("a").get("href"))
                                error = False
                            except:
                                time.sleep(wait_time)
                                print("An Error Occurred: sleeping " + str(wait_time) + "s")
                                wait_time = wait_time + 1
                                pass
                        for product in new_soup.find_all("div", class_="product-item-details"):
                            for element in product.find_all():
                                if element.get("class"):
                                    if " ".join(element.get("class")) == "price-value-wrapper":
                                        price = element.get_text().strip()
                                    stock = "In Stock"
                                    if " ".join(element.get("class")) == "product-item-title":
                                        item = element.find("a").get_text().strip()
                                        link = element.find("a").get("href")
                            sub_soup = get_html(link)
                            if sub_soup.find(class_="stock-message"):
                                stock = sub_soup.find(class_="stock-message").get_text().strip()

                            data.append({"store": name[n], "item": item, "price": price, "stock": stock, "link": link,
                                         "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                            print([name[n], item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
                            item, price, stock, link = ["", "", "", ""]

        if name[n] == "marscigars":
            soup = get_html(url[n])
            for bar in soup.find_all("table", class_="category-list"):
                # print(bar)
                for cat in bar.find_all("div", class_="category-list-item-head"):
                    error = True
                    wait_time = 2.75
                    while error:
                        try:
                            error = False
                            new_soup = get_html("http://www.marscigars.com" + cat.find("a").get("href"))
                            error = False
                        except:
                            time.sleep(wait_time)
                            print("An Error Occurred: sleeping " + str(wait_time) + "s")
                            wait_time = wait_time + 1
                            pass
                    for product in new_soup.find_all("div", class_="product-list-item"):
                        for element in product.find_all():
                            if element.get("class"):
                                if " ".join(element.get("class")) == "product-list-cost-value":
                                    priceraw = element.get_text().strip()
                                    if len(priceraw) < 7:
                                        price = priceraw
                                    else:
                                        head, sep, price = priceraw.partition("m ")
                                if " ".join(element.get("class")) == "product-list-options":
                                    item = element.find("a").get_text().strip()
                                    link = ("http://www.marscigars.com" + element.find("a").get("href"))
                                if " ".join(element.get("class")) == "product-list-control":
                                    if element.find("input"):
                                        stock = "In Stock"
                        sub_soup = get_html(link)
                        if sub_soup.find(class_="prod-detail-stock") and not stock == "In Stock":
                            stock = sub_soup.find(class_="prod-detail-stock").get_text()
                        if stock == "":
                            stock = "In Stock"

                        data.append({"store": name[n], "item": item, "price": price, "stock": stock, "link": link,
                                     "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                        print([name[n], item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
                        item, price, stock, link = ["", "", "", ""]

        if name[n] == "wilke":
            soup = get_html(url[n])
            for product in soup.find_all('ul', class_="_2Irj0"):
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

                    data.append({"store": name[n], "item": item, "price": price, "stock": stock, "link": link,
                                 "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                    print([name[n], item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
                    item, price, stock, link = ["", "", "", ""]

        if name[n] == "boswell":

            boswell_url = ["https://boswellpipes.com/product-category/boswell-tobacco/",
                           "https://boswellpipes.com/product-category/tobacco-blends/"]

            for b_url in boswell_url:

                display = Display(visible=0, size=(800, 600))
                display.start()

                try:
                    # we can now start Firefox and it will run inside the virtual display
                    browser = webdriver.Firefox()
                    browser.get(b_url)
                    browser.find_element_by_xpath(r'''//*[@id="age-verification"]/div/button[1]''').click()
                    element = browser.find_element_by_id(r'''sb-infinite-scroll-load-more''')
                    while element.text == "Load More Products":
                        element.click()
                        style = element.get_attribute("style")
                        while style == "display: none;":
                            style = browser.find_element_by_id(r'''sb-infinite-scroll-load-more''').get_attribute(
                                "style")
                        element = browser.find_element_by_id(r'''sb-infinite-scroll-load-more''')
                    soup = BeautifulSoup(browser.page_source.encode('utf8'), "lxml")
                finally:
                    # tidy-up
                    browser.quit()
                    display.stop()  # ignore any output from this.

                for product in soup.find_all("li", class_="type-product"):
                    item = product.find("h2", class_="woocommerce-loop-product__title").get_text()
                    price = product.find(class_="woocommerce-Price-amount amount").get_text()
                    link = product.find("a", class_="woocommerce-LoopProduct-link").get("href")
                    stock = "In Stock"
                    data.append({"store": "boswell", "item": item, "price": price, "stock": stock, "link": link,
                                 "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                    print([name[n], item, price, stock, link, datetime.now().strftime("%m/%d/%Y %H:%M")])
                    item, price, stock, link = ["", "", "", ""]

    return data
