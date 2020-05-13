from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "boswell"
    boswell_url = ["https://boswellpipes.com/product-category/boswell-tobacco/",
                   "https://boswellpipes.com/product-category/tobacco-blends/"]
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    for b_url in boswell_url:

        try:
            browser = webdriver.Chrome(options=chrome_options)
            browser.get(b_url)
            browser.find_element_by_xpath(r'''//*[@id="age-verification"]/div/button[1]''').click()
            links = []
            for element in browser.find_elements_by_class_name("product-category"):
                links.append(element.find_element_by_xpath(".//a").get_attribute("href"))
            for link in links:
                browser.get(link)
                html = browser.find_element_by_tag_name('html')
                loading = True
                scroll_max = 20
                scroll_count = 0
                while loading and scroll_count < scroll_max:
                    scroll_count += 1
                    html.send_keys(Keys.END)
                    time.sleep(1)
                    element_id = "sb-infinite-scroll-load-more"
                    if not browser.find_elements_by_id(element_id):
                        break
                    if browser.find_element_by_id(element_id).text == "No more products available...":
                        loading = False

                soup = BeautifulSoup(browser.page_source.encode('utf8'), "lxml")

                for product in soup.find_all("li", class_="type-product"):
                    item = product.find("h2", class_="woocommerce-loop-product__title").get_text()
                    price = product.find(class_="woocommerce-Price-amount amount").get_text()
                    link = product.find("a", class_="woocommerce-LoopProduct-link").get("href")
                    stock = "In Stock"
                    data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                                 "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                    if pbar is not None:
                        pbar.set_description(", ".join([name, item]))
                    item, price, stock, link = ["", "", "", ""]
        finally:
            # tidy-up
            browser.quit()

    return data
