from fuzzywuzzy import fuzz, process
import pickle
import re
import pandas as pd


def get_category(item, add_item=False):
    df = pickle.load(open("category_list.p", "rb"))
    if item in df["item"].values:
        tobacco = df.loc[df["item"] == item]
    else:
        review_data = []
        review_index_data = []
        for row in data:
            review_data.append(row["brand"] + " " + row["blend"])
            review_index_data.append({"brand": row["brand"], "blend": row["blend"]})
        string = simplify_string(item)
        fuzzy_blend = process.extractOne(string, review_data, scorer=fuzz.token_set_ratio)
        row = review_index_data[review_data.index(fuzzy_blend[0])]

        if add_item:
            data.append({"item": item, "brand": row["brand"], "blend": row["blend"]})
            pickle.dump(data, open("/home/TurboTAD/python/categorized_items.p", "wb"))


    return tobacco


def simplify_string(item):
    rules = [r"(?i)( (?:Tin|Bag|sold by Oz|Pouch|Bulk|Pack|Package|can)$)",
             r"(?i)( (?:\d+?\.?\d+?|\d) ?(?:oz|g|gr|Ounce|ounce|lb|LB|grams)(?:\.|,|\))?$)",
             r"(\.|,|-) ?$",
             r"(?i)(pipe tobacco)"]
    string = item
    for rule in rules:
        string = re.sub(rule, "", string)

    return string.strip()
