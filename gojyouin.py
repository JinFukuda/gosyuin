#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

url = "https://cmeg.jp/a/tags/15/castles"

res = requests.get(url)

# domにして解析する
soup = BeautifulSoup(res.content, 'html.parser')

base_url = []

for target in soup.html.find_all(class_='list_text14'):
    base_url.append(target.find('a').get("href"))


detail_base_url = "https://cmeg.jp"

name = []
address = []
type = []

for detail_target in base_url:

    # 詳細URLを作成
    detail_url = detail_base_url + detail_target

    detail_res = requests.get(detail_url)

    detail_soup = BeautifulSoup(detail_res.content, 'html.parser')

    castle_name = detail_soup.html.find(class_='font_s').find_all('table')[1].find_all('tr')[0].find_all('td')[1].text
    castle_address = ""

    i = 1
    while True:
        if detail_soup.html.find(class_='font_s').find_all('table')[1].find_all('tr')[i].find_all('td')[0].text == "所在地":
            castle_address = detail_soup.html.find(class_='font_s').find_all('table')[1].find_all('tr')[i].find_all('td')[1].text.strip()
            break
        i = i + 1

    name.append(castle_name)
    address.append(castle_address)
    type.append("お城")

dic = {
    "名称": name,
    "住所": address,
    "タイプ": type
}

df = pd.DataFrame(dic)
with pd.ExcelWriter("./gojyouin.xlsx", engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="sample_sheet", index=False)
