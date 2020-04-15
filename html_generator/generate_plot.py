import pandas as pd
import numpy as np


def generate_plot(data, brand, blend):
    # Filter DataFrame by blend
    df = data[(data.brand == brand) & (data.blend == blend)]

    # Get list of stores that have sold that blend
    string = ["data.addColumn('date', 'Date');"]
    col_string = "data.addColumn('number', '<!--STORE-->');\n\tdata.addColumn({type:'boolean',role:'certainty'});"
    stores = df.store.unique()
    for store in stores:
        string.append(col_string.replace("<!--STORE-->", store))

    # Loop over each date that blend was in stock and convert price data in google readable format
    strings = []
    for date, products in df.groupby("datetime", sort=True):
        temp_array = ["null,false"] * (len(stores) + 1)
        temp_array[0] = "".join(["new Date(", products.iloc[0]["date"], ")"])
        for index, row in products.iterrows():
            temp_array[np.where(stores == row["store"])[0][0] + 1] = row["charts-var"]
        strings.append("".join(["[", ",".join(temp_array), "]"]))

    # Create string that will be passed into js on the html page
    string.append("".join(["data.addRows([", ",".join(strings), "]);"]))
    string = "\n\t".join(string)

    return string

