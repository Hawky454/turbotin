import pandas as pd
from slugify import slugify
from tqdm import tqdm
from htmlmin import minify
import os
from html_generator.generate_plot import generate_plot
from html_generator.generate_table import generate_table
from html_generator.generate_index import generate_index


def generate_html(df, plot_data, path):
    save_path = open(os.path.join(path, "paths.txt"), "r").read()

    plot_data = clean_array(plot_data)

    index_string = generate_index(df)
    item_card = '''
            <div class="item-card">
                <div class="item-body">
                    <div class="item-body-sub">
                        <a href="<!--LINK-->" class="item-name" target="_blank"><!--NAME--></a>
                        <div class="item-time"><!--TIME--></div>
                    </div>
                    <span></span>
                    <div class="item-price-store">
                        <div class="item-price"><!--PRICE--></div>
                        <div class="item-store"><!--STORE--></div>
                    </div>
                </div>
            </div>
    '''
    replace_list = [["<!--LINK-->", "link"],
                    ["<!--NAME-->", "item"],
                    ["<!--TIME-->", "time"],
                    ["<!--PRICE-->", "price"],
                    ["<!--STORE-->", "store"]]

    data = df.groupby(['brand', 'blend'])
    files = []
    template_string = open(os.path.join(path, "templates/main_template.html"), "r").read()
    template_string = minify(template_string.replace("<!--LIST-->", index_string))
    for blend in tqdm(data, desc="Generating html"):
        url = slugify(blend[0][0] + " " + blend[0][1])
        string = template_string
        string = string.replace("<!--BLEND NAME-->", blend[0][1])
        string = string.replace("<!--TITLE-->", "Turbotin - " + blend[0][1])
        list_string = ""
        item_data = blend[1].reset_index(drop=True).T.to_dict().values()
        for row in item_data:
            try:
                row["real-price"] = float(row["price"][1:])
            except:
                row["real-price"] = float(9 * 10 ** 9)

        for row in sorted(item_data, key=lambda i: i['real-price']):
            temp_string = item_card
            if row["stock"] == "Out of stock":
                temp_string = temp_string.replace("<!--TIME-->", '''<div class="stock">Out of stock</div>''')
            for n in replace_list:
                temp_string = temp_string.replace(n[0], row[n[1]])
            list_string = list_string + "\n" + temp_string
        string = string.replace("<!--ITEM LIST-->", list_string)
        string = string.replace("<!--PLOT-->", generate_plot(plot_data, blend[0][0], blend[0][1]))
        open(os.path.join(save_path, url + ".html"), "w").write(string)
        files.append(url + ".html")

    files.append("full_table.html")
    generate_table(df, path, save_path)
    for file in os.listdir(save_path):
        if file not in files:
            os.remove(os.path.join(save_path, file))


def clean_array(df):
    df["datetime"] = pd.to_datetime(df["date"], format=r"%Y, %m, %d")
    df["day"] = df["date"].str.extract(r"\d{4}, \d{2}, (\d{2})")
    df["month"] = df["date"].str.extract(r"\d{4}, (\d{2}), \d{2}")
    df["month"] = df["month"].astype("int").add(-1)
    df["year"] = df["date"].str.extract(r"(\d{4}), \d{2}, \d{2}")
    df["date"] = "new Date(" + df["year"] + ", " + df["month"].astype("str") + ", " + df["day"] + ")"
    df = df.drop(["year", "month", "day"], axis=1)
    df["stock"] = df["stock"] != "Out of stock"
    df["charts-var"] = "{v:"+df["price"]+", f: '$"+df["price"]+"'},"+df["stock"].astype(str).str.lower()
    df = df.drop(["price", "stock"], axis=1)
    return df
