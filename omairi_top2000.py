#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import datetime

url = "https://omairi.club/spots/ranking/page/"

res = requests.get(url)

soup = BeautifulSoup(res.content, 'html.parser')

ranking = []
name = []
address = []
type = []

i = 1

finish_flag = False

while True:

    if finish_flag:
        break

    print("ページ数:" + str(i))

    # URLの作成
    url_make = url + str(i)

    # URL先のhtmlを取得する
    res = requests.get(url_make)

    # domにして解析する
    soup = BeautifulSoup(res.content, 'html.parser')

    if len(soup.html.find_all(class_='spot_ranking')) <= 0:
        break

    for target in soup.html.find_all(class_='spot_ranking'):

        # 御朱印・御城印がないところはターゲットとしない
        if target.find(class_='spot_goshuin') == None:
            continue

        ranking_data = target.find(class_='spot_rank_inner').span.text.strip()

        print("ランキングデータ:" + str(ranking_data))

        if int(ranking_data) > 2000:
            finish_flag = True
            break

        type_flag = "その他"
        if target.find(class_="l_temple"):
            type_flag = "お寺"
        elif target.find(class_="l_shrine"):
            type_flag = "神社"

        ranking.append(target.find(class_='spot_rank_inner').span.text.strip())
        name.append(target.find(class_='spot_name_body').text.replace(' ', '').strip())
        address.append(target.find(class_='spot_address').text.strip())
        type.append(type_flag)

    i = i + 1

# データをExcelに出力するう

dic = {
    'ランキング': ranking,
    '名称': name,
    '住所': address,
    'お寺・神社フラグ': type
}

df = pd.DataFrame(dic)

#ファイル名
with pd.ExcelWriter("./top_2000.xlsx", engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="sample_sheet", index=False)
