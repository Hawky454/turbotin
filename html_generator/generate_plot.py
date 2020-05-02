import pandas as pd
import numpy as np


def generate_plot(data, brand, blend):
    # Filter DataFrame by blend
    df = data[(data.brand == brand) & (data.blend == blend)]
    if df.empty:
        return ""

    # Get list of stores that have sold that blend
    string = ["data.addColumn('date', 'Date');"]
    col_string = "data.addColumn('number', '<!--STORE-->');\n\tdata.addColumn({type:'boolean',role:'certainty'});"
    stores = df.store.unique()
    for store in stores:
        string.append(col_string.replace("<!--STORE-->", store))
    df = df.sort_values("datetime")
    df = df[["date", "store", "charts-var"]]
    df = df.reset_index()
    df = df.groupby(["date", "store"])["charts-var"].aggregate("min").unstack()
    df = df.fillna("null,false")
    df["string"] = df[df.columns[0]].str.cat(df[df.columns[1:]], sep=",")
    df["string"] = "[" + df.index + "," + df["string"] + "]"

    # Create string that will be passed into js on the html page
    string.append("".join(["data.addRows([", df["string"].str.cat(sep=","), "]);"]))
    string = "\n\t".join(string)

    return string
