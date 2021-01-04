from . import get_html, add_item
import json


def scrape(pbar=None):
    item, price, stock, link = ["", "", "", ""]
    data = []
    name = "thestorytellers"
    url = "https://www.thestorytellerspipe.com/tinned-tobacco"
    soup = get_html(url)
    for category in soup.find(id="nwg8uinlineContent-gridContainer").find_all("a"):
        new_soup = get_html(category.get("href"))
        brand = category.get_text()
        for script in new_soup.find_all("script", type="text/javascript"):
            if "warmupData" in str(script):
                script = str(script).replace("\n", "")
                script = script.replace('''<script type="text/javascript">        var warmupData = ''', "")
                script = script.replace(''';    </script>''', "")
                json_data = json.loads(script)

                def find_key(search_data, key, path=None):
                    if not path:
                        path = []
                    for n in search_data:
                        if n == key:
                            return path + [n]
                        if isinstance(search_data[n], dict):
                            new_path = find_key(search_data[n], key, path=path + [n])
                            if new_path:
                                return new_path

                keys = find_key(json_data, "products")
                if not keys:
                    continue
                for n in keys:
                    json_data = json_data[n]

                for product in json_data:
                    item = " ".join([brand, product["name"]])
                    price = "${:.2f}".format(product["price"])
                    if product["isInStock"]:
                        stock = "In stock"
                    else:
                        stock = "Out of stock"
                    link = "https://www.thestorytellerspipe.com/product-page/" + product["urlPart"]
                    item, price, stock, link = add_item(data, name, item, price, stock, link, pbar)

    return data
