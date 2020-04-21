import os
import pickle
import smtplib
from email.mime.text import MIMEText

import pandas as pd
from bs4 import BeautifulSoup

# Variable allowing for relative paths
path = os.path.dirname(__file__)


def send_email(to, subject, body):
    msg = MIMEText(body, "html")
    msg['Subject'] = subject
    msg['From'] = 'Turbotin Admin <turbotinftw@gmail.com>'
    msg['To'] = to

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    password = open(os.path.join(path, "email_password.txt"), "r").read()
    server.login("turbotinftw@gmail.com", password)
    server.sendmail("turbotinftw@gmail.com", to, msg.as_string())

    # And to close server connection
    server.quit()


def send_update():
    data = pickle.load(open(os.path.join(path, "data/product_data.p"), "rb"))
    data = data[data["stock"] != "Out of stock"]
    filtered_data = data.copy()
    email_list = pd.read_csv(open(os.path.join(path, "email_list.csv"), "r"))

    for index, row in email_list.iterrows():
        timestamp, email, brand, blend = dict(row).values()
        if brand or blend:
            if brand:
                filtered_data = data[data["brand"] == brand]
            if blend:
                filtered_data = data[data["blend"] == blend]
            if not filtered_data.empty:
                key_term = ", ".join([brand, blend])
                body = generate_email_html(filtered_data, ", ".join([brand, blend]))
                subject = key_term + " is in stock"
                send_email(email, subject, body)


def generate_email_html(data, key_term):
    df = data.copy()
    df["real-price"] = data["price"].str.slice(1)
    df["real-price"] = pd.to_numeric(df["real-price"], errors="coerce")
    df = df.sort_values("real-price")
    template_string = open(os.path.join(path, "templates/email_template.html"), "r").read()
    df["name"] = r'''<a target="blank" href="''' + df["link"] + '''">''' + df["item"] + '''</a>'''
    df = df[["store", "name", "stock", "price", "time"]]
    df.columns = [n[0].upper() + n[1:] for n in df.columns]
    string = template_string.replace("<!--TABLE-->", df.to_html(index=False, justify="left", escape=False))
    string = string.replace(r'''border="1" class="dataframe"''',
                            r'''border="0" id="table" class="tablesorter custom-table"''')
    string = string.replace("<!--BLEND NAME-->", key_term)

    return string
