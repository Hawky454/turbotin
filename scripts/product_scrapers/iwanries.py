from . import get_html, add_item
import time


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "iwanries"
    url = "https://www.iwanries.com/Import-Domestic-Tobacco-C14.cfm"

    soup = get_html(url)
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

                    item, price, stock, link = add_item(data, name, item, price, stock, link, pbar)

    return data
