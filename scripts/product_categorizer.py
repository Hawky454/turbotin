import re
from tqdm import tqdm
import os
import pandas as pd


def get_category(item, cat_data, review_data):
    if item in cat_data["item"].values:
        tobacco = cat_data.loc[cat_data["item"] == item]
        contains_item = True
    else:
        from fuzzywuzzy import fuzz, process
        string = simplify_string(item)
        fuzzy_blend = process.extractOne(string, review_data["full_name"].tolist(), scorer=fuzz.token_set_ratio)
        tobacco = review_data.loc[review_data["full_name"] == fuzzy_blend[0]]
        contains_item = False

    return {"brand": tobacco["brand"].iloc[0], "blend": tobacco["blend"].iloc[0]}, contains_item


def simplify_string(item):
    rules = [r"(?i)( (?:Tin|Bag|sold by Oz|Pouch|Bulk|Pack|Package|can)$)",
             r"(?i)( (?:\d+?\.?\d+?|\d) ?(?:oz|g|gr|Ounce|ounce|lb|LB|grams)(?:\.|,|\))?$)",
             r"(\.|,|-) ?$",
             r"(?i)(pipe tobacco)"]
    string = item
    for rule in rules:
        string = re.sub(rule, "", string)

    return string.strip()


def categorize(filename):
    # Variable allowing for relative paths
    path = os.path.dirname(os.path.dirname(__file__))
    product_data = pd.read_feather(filename)
    review_data = pd.read_feather(os.path.join(path, "data/review_data.feather"))
    cat_data = pd.read_feather(os.path.join(path, "data/cat_data.feather"))
    product_data["brand"] = ""
    product_data["blend"] = ""
    product_data = product_data.reset_index(drop=True)
    for index, row in tqdm(product_data.iterrows(), total=product_data.shape[0], desc="Categorizing tobacco"):
        tobacco, contains_item = get_category(row["item"], cat_data, review_data)
        product_data.at[index, "brand"] = tobacco["brand"]
        product_data.at[index, "blend"] = tobacco["blend"]
        if not contains_item:
            cat_data = cat_data.append({"item": row["item"], "brand": tobacco["brand"], "blend": tobacco["blend"]},
                                       ignore_index=True)
    product_data = product_data.reset_index(drop=True)
    product_data.to_feather(filename)
    cat_data = cat_data.reset_index(drop=True)
    cat_data.to_feather(os.path.join(path, "data/cat_data.feather"))
