import urllib.request as request
from bs4 import BeautifulSoup
from requests_html import HTMLSession


def get_html(url):
    req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = request.urlopen(req)
    return BeautifulSoup(response.read(), features="lxml")


def get_js(url):
    js_session = HTMLSession()
    js_response = js_session.get(url)
    js_response.html.render(timeout=16000)
    return BeautifulSoup(js_response.html.html, features="lxml")
