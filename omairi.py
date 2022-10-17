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
#goshuin_flg = []

i = 1

while True :

    print(i)

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

        # 寺・神社フラグ
        target_flag = "その他"
        if target.find(class_="l_temple"):
            target_flag = "お寺"
        elif target.find(class_="l_shrine"):
            target_flag = "神社"

        # 御朱印フラグ
#        goshin_flag = 0
#        if target.find(class_='spot_goshuin'):
#            goshin_flag = 1

        ranking.append(target.find(class_='spot_rank_inner').span.text.strip())
        name.append(target.find(class_='spot_name_body').text.replace(' ', '').strip())
        address.append(target.find(class_='spot_address').text.strip())
        type.append(target_flag)
#        goshuin_flg.append(goshin_flag)

    i = i + 1


dic = {
    'ランキング': ranking,
    '名称': name,
    '住所': address,
    '神社・寺フラグ': type
#    '御朱印フラグ': goshuin_flg
}

df = pd.DataFrame(dic)

file_path = os.getcwd() + "\\" + "data_file.xslx"
with pd.ExcelWriter("./sample.xlsx", engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="sample_sheet", index=False)
