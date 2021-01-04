from selenium import webdriver
from bs4 import BeautifulSoup
from . import add_item


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "ljperetti"
    url = "https://www.ljperetti.com/tobacco"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    try:
        browser = webdriver.Chrome(options=chrome_options)
        browser.get(url)
        if browser.find_elements_by_class_name("age-button"):
            browser.find_element_by_class_name("age-button").click()
            browser.get(url)
        links = []
        for element in browser.find_elements_by_class_name("ljp-sidebar-link"):
            links.append(element.get_attribute("href"))
        for main_link in links:
            browser.get(main_link)
            soup = BeautifulSoup(browser.page_source.encode('utf8'), "lxml")
            if soup.find_all(class_="note-msg-empty-catalog"):
                continue
            for product in soup.find("ol", class_="products-list").find_all("li"):
                if not product.find_all("h2", class_="product-name"):
                    continue
                item = product.find("h2", class_="product-name").get_text()
                price = product.find("span", class_="price")
                if price:
                    price = price.get_text().strip()
                    stock = "In stock"
                else:
                    stock = "Out of stock"
                link = main_link
                item, price, stock, link = add_item(data, name, item, price, stock, link, pbar)
    finally:
        # tidy-up
        browser.quit()

    return data
