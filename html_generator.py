import pickle
import pandas as pd
from datetime import datetime
from slugify import slugify
from tqdm import tqdm
from htmlmin import minify
import os
import numpy as np

href_path = r""
save_path = r"html_pages/"


def generate_index(df):
    brands = df.groupby(["brand"])
    main_string = ""
    brand_string = '''
    <div class="list-brand">
        <div class="collapsible" id="<!--PARENT-->" data-num="<!--NUM-->">
            <div style="white-space: nowrap; overflow: hidden;"><!--BRAND--></div>
            <span></span>
            <i class="fa fa-caret-down" style="float: right;"></i>
        </div>
        <div class="content" id="<!--PARENT-->-child">
            <!--BLENDS-->
        </div>
    </div>
    '''
    blend_string = '''
    <div class="content-text" onclick="saveScroll('<!--LINK-->', '<!--PARENT-->')"><!--BLEND--></div>
    '''
    counter = 0
    for brand in sorted(brands, key=lambda i: i[0]):
        counter = counter + 1
        custom_id = slugify(str(counter) + " " + brand[0])
        temp_string = brand_string.replace("<!--BRAND-->", brand[0]) \
            .replace("<!--PARENT-->", custom_id) \
            .replace("<!--NUM-->", str(counter))
        sub_temp_string = ""
        for blend in sorted(brand[1].blend.unique()):
            sub_temp_string = sub_temp_string + blend_string \
                .replace("<!--LINK-->", href_path + slugify(brand[0] + " " + blend) + ".html") \
                .replace("<!--BLEND-->", blend) \
                .replace("<!--PARENT-->", custom_id)
        temp_string = temp_string.replace("<!--BLENDS-->", sub_temp_string)
        main_string = main_string + "\n" + temp_string
    return main_string


def generate_html(df, plot_data):
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
    for blend in tqdm(data, desc="Generating html"):
        url = slugify(blend[0][0] + " " + blend[0][1])
        string = open("templates/main_template.html", "r").read()
        string = string.replace("<!--BLEND NAME-->", blend[0][1])
        string = string.replace("<!--TITLE-->", "Turbotin - " + blend[0][1])
        list_string = ""
        item_data = blend[1].reset_index().T.to_dict().values()
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
        string = string.replace("<!--LIST-->", index_string)
        open(save_path + url + ".html", "w").write(string)
        files.append(url + ".html")

    for file in os.listdir(save_path):
        if file not in files:
            os.remove(save_path+file)


def generate_plot(data, brand, blend):
    df = data[(data.brand == brand) & (data.blend == blend)]

    string = ["data.addColumn('date', 'Date');"]
    col_string = "data.addColumn('number', '<!--STORE-->');"
    stores = df.store.unique()
    for store in stores:
        string.append(col_string.replace("<!--STORE-->", store))

    strings = []
    value_string = "{v:d, f: '$d'}"
    temp_array = ["null"] * (len(stores) + 1)
    for date, products in df.groupby("date"):
        temp_array[0] = "".join(["new Date(", date, ")"])
        for index, row in products.iterrows():
            temp_array[np.where(stores == row["store"])[0][0]+1] = value_string.replace("d", row["price"])
        strings.append("".join(["[", ",".join(temp_array), "]"]))

    string.append("".join(["data.addRows([", ",".join(strings), "]);"]))
    string = "\n\t".join(string)

    return string
