from fuzzywuzzy import fuzz, process
import pickle
import re
import pandas as pd


def get_category(item, add_item=False, cat_data=False, review_data=False):
    if not cat_data:
        cat_data = pickle.load(open("category_list.p", "rb"))
    if item in cat_data["item"].values:
        tobacco = cat_data.loc[cat_data["item"] == item]
    else:
        if not review_data:
            review_data = pickle.load(open("review_data.p", "rb"))
        string = simplify_string(item)
        fuzzy_blend = process.extractOne(string, review_data["full_name"].tolist(), scorer=fuzz.token_set_ratio)
        tobacco = review_data.loc[review_data["full_name"] == fuzzy_blend[0]]
        if add_item:
            cat_data.append({"item": item, "brand": tobacco["brand"], "blend": tobacco["blend"]})
            pickle.dump(cat_data, open("category_list.p", "wb"))

    return {"brand": tobacco["brand"].iloc[0], "blend": tobacco["blend"].iloc[0]}


def simplify_string(item):
    rules = [r"(?i)( (?:Tin|Bag|sold by Oz|Pouch|Bulk|Pack|Package|can)$)",
             r"(?i)( (?:\d+?\.?\d+?|\d) ?(?:oz|g|gr|Ounce|ounce|lb|LB|grams)(?:\.|,|\))?$)",
             r"(\.|,|-) ?$",
             r"(?i)(pipe tobacco)"]
    string = item
    for rule in rules:
        string = re.sub(rule, "", string)

    return string.strip()
