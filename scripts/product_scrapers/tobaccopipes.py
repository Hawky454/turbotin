from datetime import datetime
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "tobaccopipes"
    url = "https://www.tobaccopipes.com/pipe-tobacco"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    browser = webdriver.Chrome(options=chrome_options)

    try:
        next_page = True
        browser.get(url)
        while next_page:
            skeleton_error = True
            max_tries = 20
            num_tries = 0
            while skeleton_error and num_tries < max_tries:
                num_tries += 1
                time.sleep(2)
                browser.refresh()
                soup = BeautifulSoup(browser.page_source.encode('utf8'), "lxml")
                skeleton_error = False
                for product in soup.find_all("li", class_="isp_grid_product"):
                    if "isp_sold_out_banner" in str(product):
                        stock = "Out of stock"
                    else:
                        stock = "In stock"
                    if "<!-- skeleton -->" in str(product):
                        skeleton_error = True
                        time.sleep(5)
                        break
                    link = "https://www.tobaccopipes.com" + product.find("a").get("href")
                    item = product.find(class_="isp_product_title").get_text()
                    price = product.find(class_="isp_product_price_wrapper").get_text()
                    if re.match(r"\$\d+\.\d{2} \$\d+\.\d{2}", price):
                        price = re.findall(r"\$\d+\.\d{2} (\$\d+\.\d{2})", price)[0]

                    data.append({"store": name, "item": item, "price": price, "stock": stock, "link": link,
                                 "time": datetime.now().strftime("%m/%d/%Y %H:%M")})
                    if pbar is not None:
                        pbar.set_description(", ".join([name, item]))
                    item, price, stock, link = ["", "", "", ""]
            if browser.find_elements_by_xpath('''//li[@class='page-item next disabled']'''):
                next_page = False
            else:
                browser.find_element_by_xpath('''//*[@id="isp_pagination_anchor"]/ul/li[7]/a''').click()

    except Exception as e:
        print(e)
        browser.quit()
    finally:
        browser.quit()

    return data
