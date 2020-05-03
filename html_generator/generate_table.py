import os
from bs4 import BeautifulSoup
from htmlmin import minify


def generate_table(df, path, save_path):
    template_string = open(os.path.join(path, "templates/table_template.html"), "r").read()
    header = open(os.path.join(path, "templates/header.html"), "r").read()
    template_string = template_string.replace("<!--HEADER-->", header)

    df["name"] = r'''<a target="blank" href="''' + df["link"] + '''">''' + df["item"] + '''</a>'''
    df = df[["store", "name", "stock", "price", "time"]]
    df.columns = [n[0].upper() + n[1:] for n in df.columns]
    string = template_string.replace("<!--TABLE-->", df.to_html(index=False, justify="left", escape=False))
    string = string.replace(r'''border="1" class="dataframe"''',
                            r'''border="0" id="table" class="tablesorter custom-table"''')

    # Specify rows that are out of stock
    soup = BeautifulSoup(string, features="lxml")
    for i in soup.find_all("tr"):
        if "Out of stock" in str(i):
            i["class"] = "out-of-stock"

    open(os.path.join(save_path, "full_table.html"), "w").write(minify(str(soup)))
