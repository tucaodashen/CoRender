import os
import time
from urllib.parse import unquote
from faker import Faker

import requests

def downlowdBl(url,filename):
    r = requests.get(url, stream=True)
    with open(filename, "wb") as Pypdf:
        for chunk in r.iter_content(chunk_size=1024):  # 1024 bytes
            if chunk:
                Pypdf.write(chunk,)
uas = Faker()
ua = uas.user_agent()
headers = {'user-agent': ua}


def get_file_name(url, headers):
    filename = ''
    if 'Content-Disposition' in headers and headers['Content-Disposition']:
        disposition_split = headers['Content-Disposition'].split(';')
        if len(disposition_split) > 1:
            if disposition_split[1].strip().lower().startswith('filename='):
                file_name = disposition_split[1].split('=')
                if len(file_name) > 1:
                    filename = unquote(file_name[1])
    if not filename and os.path.basename(url):
        filename = os.path.basename(url).split("?")[0]
    if not filename:
        return time.time()
    return filename

def download(url):
    try:
        filename = get_file_name(url, headers)
        downlowdBl(url,filename)
        return str(filename)
    except:
        return False
