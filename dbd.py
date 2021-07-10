from bs4 import BeautifulSoup
from requests import get
import csv
import os
import re

DBD_BASE_URL = "https://www.dbd.go.th/"
DATA_PATH = "./data/"

CSV_HEADERS = {
    "1": [
        "ลำดับ",
        "เลขทะเบียน",
        "ชื่อนิติบุคคล",
        "วันที่จดทะเบียน",
        "ทุนจดทะเบียน",
        "รหัสวัตถุประสงค์",
        "รายละเอียดวัตถุประสงค์",
        "ที่ตั้งสำนักงานใหญ่",
        "ตำบล",
        "อำเภอ",
        "จังหวัด",
        "รหัสไปรษณีย์",
    ],
    "2": [
        "ลำดับ",
        "เลขทะเบียน",
        "ชื่อนิติบุคคล",
        "วันที่จดเลิก",
        "ทุนจดทะเบียน (บาท)",
        "รหัสวัตถุประสงค์",
        "รายละเอียดวัตถุประสงค์",
        "ที่ตั้งสำนักงานใหญ่",
        "ตำบล",
        "อำเภอ",
        "จังหวัด",
        "รหัสไปรษณีย์",
    ],
}


def process_dbd_csv():
    fs = get_downloaded_files()
    data = {"1": [], "2": []}
    for i in fs:
        key, result = dbd_csv_processor(i)
        data[key] += result
    return data


def dbd_csv_processor(fp):
    res = re.findall("_(\d)\.csv$", fp)
    if not res:
        return None, []
    data = []
    _type = res[0]
    with open(fp, "rt") as f:
        cf = csv.reader(f)
        for row in cf:
            order = row[0].replace(",", "")
            # get rid of any irrelevent row
            try:
                int(order)
            except ValueError:
                continue
            row = [i.strip() for i in row]
            one_row = list(zip(CSV_HEADERS[_type], row))
            data.append(one_row)
    return _type, data


def get_downloaded_files():
    result = []
    for base_path, _, files in os.walk(DATA_PATH):
        for fi in files:
            if fi.find(".csv") == -1:
                continue
            fp = os.path.join(base_path, fi)
            result.append(fp)
    return result


def get_dbd_csv(url):
    res = get(url)
    if res.status_code != 200:
        print(f"URL error: {res.status_code} URL = {url}")
        return
    res.encoding = "utf-8"
    html = res.text
    # tree = etree.parse(StringIO(html), parser)
    page = BeautifulSoup(html, "html.parser")
    # print(page)
    tab = page.find("table")
    for row in tab.find_all("tr"):
        children = row.children
        if len(list(children)) != 13:
            continue
        # print(f"--{month}--")
        for link in row.find_all("a"):
            href = link.attrs["href"]
            if href.find(".csv") == -1:
                continue
            # print(f"link: {href}  --  {new_found}")
            fp = os.path.basename(href)
            if check_if_already_fetched(fp):
                continue
            # fetch file and save to DATA_PATH
            result = download_file(href, fp)
            # print(f"result: {result}")
        # print(f'row col # {len(list(children))}')


def download_file(url, fp):
    full_path = os.path.join(DATA_PATH, fp)
    with open(full_path, "wt") as f:
        res = get(f"{DBD_BASE_URL}{url}")
        if res.status_code != 200:
            return False
        res.encoding = "utf-8"
        f.write(res.text)
    return full_path


def check_if_already_fetched(fp):
    full_path = os.path.join(DATA_PATH, fp)
    return os.path.exists(full_path)
