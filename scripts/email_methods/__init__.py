import os
import pickle
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import pandas as pd

# Variable allowing for relative paths
path = os.path.dirname(__file__)
path = os.path.dirname(path)


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


def send_update(test=False):
    with open(os.path.join(path, "data/product_data.p"), "rb") as f:
        data = pickle.load(f)
    data = data[data["stock"] != "Out of stock"]
    filtered_data = data.copy()
    with open(os.path.join(path, "email_methods/email_list.csv"), "r") as f:
        email_list = pd.read_csv(f)

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
                if not test:
                    send_email(email, subject, body)
                subject += ", sent to " + email
                if test:
                    subject += ", (run as test)"
                send_email("turbotinftw@gmail.com", subject, body)


def generate_email_html(data, key_term):
    df = data.copy()
    df["real-price"] = data["price"].str.slice(1)
    df["real-price"] = pd.to_numeric(df["real-price"], errors="coerce")
    df = df.sort_values("real-price")
    with open(os.path.join(path, "templates/email_template.html"), "r") as f:
        template_string = f.read()
    df["name"] = r'''<a target="blank" href="''' + df["link"] + '''">''' + df["item"] + '''</a>'''
    df = df[["store", "name", "stock", "price", "time"]]
    df.columns = [n[0].upper() + n[1:] for n in df.columns]
    string = template_string.replace("<!--TABLE-->", df.to_html(index=False, justify="left", escape=False))
    string = string.replace(r'''border="1" class="dataframe"''',
                            r'''border="0" id="table" class="tablesorter custom-table"''')
    string = string.replace("<!--BLEND NAME-->", key_term)

    return string


def send_log_email(log_data):
    with open(os.path.join(path, "templates/email_template.html"), "r") as f:
        template_string = f.read()
    log_email = template_string.replace("<!--TABLE-->", log_data.to_html(index=False, justify="left", escape=False))
    log_email = log_email.replace(r'''border="1" class="dataframe"''',
                                  r'''border="0" id="table" class="tablesorter custom-table"''')

    # Specify rows that are errors
    soup = BeautifulSoup(log_email, features="lxml")
    tr = soup.find_all("tr")
    for i in range(1, len(tr)):
        if log_data["products"].iloc[i - 1] == 0 or isinstance(log_data["error"].iloc[i - 1], str):
            for td in tr[i].find_all("td"):
                td["style"] = "color:rgba(255,0,0, 1)"
    send_email("turbotinftw@gmail.com", "Website Updated", str(soup))


def send_email_confirmation_code(email, url):
    subject = "Your email verification code for turbotin.com"
    body = "Go to this url to verify your email address: {}".format(url)
    send_email(email, subject, body)
