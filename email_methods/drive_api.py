from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import os


def get_drive_data():
    path = os.path.dirname(__file__)
    SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
    store = file.Storage(os.path.join(path, 'storage.json'))
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(os.path.join(path, 'client_id.json'), SCOPES)
        creds = tools.run_flow(flow, store, http=Http(disable_ssl_certificate_validation=True))
    DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http(disable_ssl_certificate_validation=True)))

    file_id = "1XUYtYErYcVZFsyQzqiG72YX8L04WHEAAObMFS6PLiAo"
    mimeType = "text/csv"
    data = DRIVE.files().export(fileId=file_id, mimeType=mimeType).execute()
    with open(os.path.join(path, "email_list.csv"), "wb") as f:
        f.write(data)
