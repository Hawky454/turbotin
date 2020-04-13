import pickle
import pandas as pd
from slugify import slugify
from tqdm import tqdm
from htmlmin import minify
import os
import numpy as np
from bs4 import BeautifulSoup


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
                .replace("<!--LINK-->", slugify(brand[0] + " " + blend) + ".html") \
                .replace("<!--BLEND-->", blend) \
                .replace("<!--PARENT-->", custom_id)
        temp_string = temp_string.replace("<!--BLENDS-->", sub_temp_string)
        main_string = main_string + "\n" + temp_string
    return main_string


def generate_html(df, plot_data):
    # Variable allowing for relative paths
    path = os.path.dirname(__file__)
    save_path = eval(open(os.path.join(path, "paths.txt"), "r").read()).values()

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


def generate_plot(data, brand, blend):
    # Filter DataFrame by blend
    df = data[(data.brand == brand) & (data.blend == blend)]

    # Get list of stores that have sold that blend
    string = ["data.addColumn('date', 'Date');"]
    col_string = "data.addColumn('number', '<!--STORE-->');\n\tdata.addColumn({type:'boolean',role:'scope'});"
    stores = df.store.unique()
    for store in stores:
        string.append(col_string.replace("<!--STORE-->", store))

    # Loop over each date that blend was in stock and convert price data in google readable format
    strings = []
    temp_array = ["null,false"] * (len(stores) + 1)
    for date, products in df.groupby("datetime", sort=True):
        temp_array[0] = "".join(["new Date(", products.iloc[0]["date"], ")"])
        for index, row in products.iterrows():
            temp_array[np.where(stores == row["store"])[0][0] + 1] = row["charts-var"]
        strings.append("".join(["[", ",".join(temp_array), "]"]))

    # Create string that will be passed into js on the html page
    string.append("".join(["data.addRows([", ",".join(strings), "]);"]))
    string = "\n\t".join(string)

    return string


def generate_table(df, path, save_path):
    template_string = open(os.path.join(path, "templates/table_template.html"), "r").read()
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


def clean_array(df):
    df["datetime"] = pd.to_datetime(df["date"], format=r"%Y, %m, %d")
    df["day"] = df["date"].str.extract(r"\d{4}, \d{2}, (\d{2})")
    df["month"] = df["date"].str.extract(r"\d{4}, (\d{2}), \d{2}")
    df["month"] = df["month"].astype("int").add(-1)
    df["year"] = df["date"].str.extract(r"(\d{4}), \d{2}, \d{2}")
    df["date"] = df["year"] + ", " + df["month"].astype("str") + ", " + df["day"]
    df = df.drop(["year", "month", "day"], axis=1)
    df["stock"] = df["stock"] != "Out of stock"
    df["charts-var"] = "{v:"+df["price"]+", f: '$"+df["price"]+"'},"+df["stock"].astype(str).str.lower()
    df = df.drop(["price", "stock"], axis=1)
    return df
