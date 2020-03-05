import pickle
import urllib.request as request
from bs4 import BeautifulSoup


def get_html(url):
    req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = request.urlopen(req)
    return BeautifulSoup(response.read(), features="lxml")


def get_reviews(url):
    review_data = []
    soup = get_html(url)
    for tr in soup.find_all("tr"):
        if tr.find("a"):
            sub_soup = get_html(r"https://www.tobaccoreviews.com" + tr.find("a").get("href"))
            blends = []
            for sub_tr in sub_soup.find_all("tr"):
                if sub_tr.find("a") and sub_tr.find("a").get("href") != "#reviews":
                    blends.append({"name": sub_tr.find("a").get_text(),
                                   "link": r"https://www.tobaccoreviews.com" + sub_tr.find("a").get("href"),
                                   "score": sub_tr.find_all("td")[2].get_text(),
                                   "brand_link": r"https://www.tobaccoreviews.com" + tr.find("a").get("href")})
            if blends:
                review_data.append({"brand": tr.find("a").get_text(), "blends": blends})
                print(str(tr.find("a").get_text()) + " " + str(blends))

    return review_data
