from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "kbven"
    urls = ["https://kbven.com/product-category/kbb/",
            "https://kbven.com/product-category/opb"]
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    for url in urls:

        try:
            browser = webdriver.Chrome(options=chrome_options)
            browser.get(url)
            html = browser.find_element_by_tag_name('html')
            scroll_max = 100
            scroll_count = 0
            products = 0
            while scroll_count < scroll_max:
                scroll_count += 1
                soup = BeautifulSoup(browser.page_source.encode('utf8'), "lxml")
                if products == len(soup.find("ul", class_="products").find_all("li")):
                    break
                products = len(soup.find("ul", class_="products").find_all("li"))
                for i in range(10):
                    html.send_keys(Keys.END)
                    time.sleep(1)

            for product in soup.find_all("div", class_="product-content-inner"):
                item = product.find("h3").get_text()
                if url == "https://kbven.com/product-category/kbb/":
                    item = "KBVEN " + item
                price = product.find(class_="price").get_text()
                link = product.find("a").get("href")
                parent = product.parent
                while parent.name != "li":
                    parent = parent.parent
                if "Out of Stock" in parent.get_text():
                    stock = "Out of stock"
                else:
                    stock = "In stock"
                data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                             "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                if pbar is not None:
                    pbar.set_description(", ".join([name, item]))
                item, price, stock, link = ["", "", "", ""]
        finally:
            # tidy-up
            browser.quit()

    return data
