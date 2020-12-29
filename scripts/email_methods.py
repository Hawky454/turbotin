import os
import smtplib
from email.mime.text import MIMEText
import pandas as pd
import json

# Variable allowing for relative paths
path = os.path.dirname(os.path.dirname(__file__))


def send_email(to, subject, body):
    msg = MIMEText(body, "html")
    msg['Subject'] = subject
    msg['From'] = 'Turbotin Admin <turbotinftw@gmail.com>'
    msg['To'] = to

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login("turbotinftw@gmail.com", os.environ["EMAIL_PASSWORD"])
    server.sendmail("turbotinftw@gmail.com", to, msg.as_string())

    # And to close server connection
    server.quit()


def send_update(data, users):
    data = data.copy()
    data["price_num"] = data["price"].str.extract(r'(\d+.\d+)')
    data["price_num"] = pd.to_numeric(data["price_num"], errors="coerce").fillna(10 ** 4)
    data = data[data["stock"] != "Out of stock"]
    for index, row in users.iterrows():
        updates = json.loads(row["email_updates"])
        for update in updates:
            brand = update["brand"]
            blend = update["blend"]
            filtered_data = data[data["brand"] == brand]
            filtered_data = filtered_data[filtered_data["blend"] == blend]
            if update["stores"]:
                filtered_data = filtered_data[filtered_data["store"].isin(update["stores"])]
            if update["max_price"]:
                filtered_data = filtered_data[filtered_data["price_num"] < update["max_price"]]
            if not filtered_data.empty:
                subject = "{brand} {blend} is in stock".format(brand=brand, blend=blend)
                body = "See where {blend} is in stock, or manage your notifications on <a " \
                       "href='turbotin.com/email_updates'>TurboTin.com</a>".format(blend=blend)
                send_email(row["email"], subject, body)


def send_log_email(log_data):
    send_email("turbotinftw@gmail.com", "Website Updated", log_data.to_html())
