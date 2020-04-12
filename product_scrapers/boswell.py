from datetime import datetime
from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "boswell"
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
            if pbar is not None:
                pbar.set_description(", ".join([name, item]))
            item, price, stock, link = ["", "", "", ""]

    return data
