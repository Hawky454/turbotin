import pickle
import pandas as pd
from datetime import datetime
from slugify import slugify
from tqdm import tqdm

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


def generate_plot(data, brand, blend):
    df = data[(data.brand == brand) & (data.blend == blend) & (data.price != "")]

    string = "data.addColumn('date', 'Date');\n"
    col_string = "data.addColumn('number', '<!--STORE-->');\n"
    stores = df.store.unique()
    for store in stores:
        string = string + col_string.replace("<!--STORE-->", store)

    data_string = ""
    for time in df["time"].unique():
        df_time = df[df["time"] == time]
        temp_string = "[new Date(" + datetime.strptime(time, "%m/%d/%Y %H:%M").strftime("%Y, %m, %d") + ")"
        for store in stores:
            temp_string = temp_string + ","
            try:
                price = str(float(df_time[df_time.store == store].price.iloc[0][1:]))
                temp_string = temp_string + "{v:" + price + ", f: '$" + price + "'}"
            except:
                temp_string = temp_string + "null"
                pass
        data_string = data_string + temp_string + "],"
    data_string = "data.addRows([" + data_string[:len(data_string) - 1] + "]);"

    string = string + "\n" + data_string
    return string
