import os
from bs4 import BeautifulSoup
from htmlmin import minify


def generate_table(df, path, save_path):
    with open(os.path.join(path, "templates/table_template.html"), "r") as f:
        template_string = f.read()
    with open(os.path.join(path, "templates/header.html"), "r") as f:
        header = f.read()
    template_string = template_string.replace("<!--HEADER-->", header)
    template_string = template_string.replace("<!--TITLE-->", "TurboTin")

    df["name"] = r'''<a target="blank" href="''' + df["link"] + '''">''' + df["item"] + '''</a>'''
    df = df[["store", "name", "stock", "price", "time"]]
    df.columns = [n[0].upper() + n[1:] for n in df.columns]
    string = template_string.replace("<!--TABLE-->", df.to_html(index=False, justify="left", escape=False))
    string = string.replace(r'''border="1" class="dataframe"''',
                            r'''border="0" id="table" class="tablesorter custom-table"''')

    # Specify rows that are out of stock
    soup = BeautifulSoup(string, features="lxml")
    rows = soup.find_all("tr")
    for th in rows[0].find_all("th"):
        th["data-placeholder"] = "Search..."
    for row in rows:
        if "Out of stock" in str(row):
            row["class"] = "out-of-stock"
    with open(os.path.join(save_path, "full_table.html"), "w", encoding="utf-8") as f:
        f.write(minify(str(soup)))
