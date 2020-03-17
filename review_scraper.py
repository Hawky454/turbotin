from tqdm import tqdm
import urllib.request as request
from bs4 import BeautifulSoup


def get_html(url):
    req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = request.urlopen(req)
    return BeautifulSoup(response.read(), features="lxml")


def get_reviews(url):
    review_data = []
    soup = get_html(url)
    for tr in tqdm(soup.find_all("tr")):
        if tr.find("a"):
            sub_soup = get_html(r"https://www.tobaccoreviews.com" + tr.find("a").get("href"))
            for sub_tr in sub_soup.find_all("tr"):
                if sub_tr.find("a") and sub_tr.find("a").get("href") != "#reviews":
                    brand = tr.find("a").get_text()
                    blend = sub_tr.find("a").get_text()
                    review_data.append({"brand": brand,
                                        "blend": blend,
                                        "link": r"https://www.tobaccoreviews.com" + sub_tr.find("a").get("href"),
                                        "score": sub_tr.find_all("td")[2].get_text(),
                                        "brand_link": r"https://www.tobaccoreviews.com" + tr.find("a").get("href"),
                                        "full_name": brand + " " + blend})

    return review_data
