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

temple_ranking = []
temple_name = []
temple_address = []

shrine_ranking = []
shrine_name = []
shrine_address = []

other_ranking = []
other_name = []
other_address = []

type = []



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
            temple_ranking.append(target.find(class_='spot_rank_inner').span.text.strip())
            temple_name.append(target.find(class_='spot_name_body').text.replace(' ', '').strip())
            temple_address.append(target.find(class_='spot_address').text.strip())
        elif target.find(class_="l_shrine"):
            shrine_ranking.append(target.find(class_='spot_rank_inner').span.text.strip())
            shrine_name.append(target.find(class_='spot_name_body').text.replace(' ', '').strip())
            shrine_address.append(target.find(class_='spot_address').text.strip())
        else :
            other_ranking.append(target.find(class_='spot_rank_inner').span.text.strip())
            other_name.append(target.find(class_='spot_name_body').text.replace(' ', '').strip())
            other_address.append(target.find(class_='spot_address').text.strip())

    i = i + 1

print("temple:" + str(len(temple_ranking)))
print("shrine:" + str(len(shrine_ranking)))
print("other:" + str(len(other_ranking)))

# データ出力

# お寺
max = 1900
max_count = int(len(temple_ranking) / max) + 1

for count in range(max_count):

    print("count:" + str(count))

    start = count * max
    end = (count + 1) * 1900

    ranking = temple_ranking[start:end]
    name = temple_name[start:end]
    address = temple_address[start:end]

    dic = {
        'ランキング': ranking,
        '名称': name,
        '住所': address
    }

    df = pd.DataFrame(dic)

    #ファイル名
    with pd.ExcelWriter("./temple_" + str(count) + ".xlsx", engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="sample_sheet", index=False)


# 神社
max_count = int(len(shrine_ranking) / max) + 1

for count in range(max_count):

    start = count * max
    end = (count + 1) * 1900

    ranking = shrine_ranking[start:end]
    name = shrine_name[start:end]
    address = shrine_address[start:end]

    dic = {
        'ランキング': ranking,
        '名称': name,
        '住所': address
    }

    df = pd.DataFrame(dic)

    #ファイル名
    with pd.ExcelWriter("./shrine_" + str(count) + ".xlsx", engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="sample_sheet", index=False)

# その他
max_count = int(len(other_ranking) / max) + 1

for count in range(max_count):

    start = count * max
    end = (count + 1) * 1900

    ranking = other_ranking[start:end]
    name = other_name[start:end]
    address = other_address[start:end]

    dic = {
        'ランキング': ranking,
        '名称': name,
        '住所': address
    }

    df = pd.DataFrame(dic)

    #ファイル名
    with pd.ExcelWriter("./other_" + str(count) + ".xlsx", engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="sample_sheet", index=False)
