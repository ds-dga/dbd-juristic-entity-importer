import datetime
import tempfile
import csv
import os
from pprint import pprint
from requests import Session
from dbd import CSV_HEADERS

"""
Example: CKAN API usage

curl -X POST  -H "Content-Type: multipart/form-data"  -H "Authorization: XXXX"  -F "id=<resource_id>" -F "upload=@updated_file.csv" https://demo.ckan.org/api/3/action/resource_patch

"""


def push2ckan(conf, data, ckan_config):
    for k in data.keys():
        # prep for file to upload
        fname = None
        with tempfile.NamedTemporaryFile(
            delete=False, mode="w+t", encoding="utf-8"
        ) as f:
            fname = f.name
            cf = csv.DictWriter(f, fieldnames=CSV_HEADERS[k])
            cf.writeheader()
            cf.writerows([dict(r) for r in data[k]])
        # print("filename: ", fname)
        url = f"{ckan_config['base_url']}/resource_update"
        today = datetime.date.today().strftime("%Y-%m-%d")
        multipart_form_data = {
            "id": (None, conf[k]["resource_id"]),
            "name": (None, conf[k]["title"]),
            "upload": (f"{conf[k]['title']}-{today}.csv", open(fname, "rt")),
        }
        s = Session()
        s.headers = {
            "Authorization": ckan_config["api_key"],
        }
        resp = s.post(url, files=multipart_form_data)
        pprint(str(resp.text))
        f.close()
        os.unlink(fname)
