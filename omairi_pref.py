#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import datetime
import sys


# エリアパラメータ
area = sys.argv[1]
print(area)

if area == "1":
    # 北海道
    url = [
        "https://omairi.club/pref/hokkaido/page/"
    ]
    file_name = "hokkaidou_"

elif area == "2":
    # 東北
    url = [
        "https://omairi.club/pref/aomori/page/",
        "https://omairi.club/pref/iwate/page/",
        "https://omairi.club/pref/miyagi/page/",
        "https://omairi.club/pref/akita/page/",
        "https://omairi.club/pref/yamagata/page/",
        "https://omairi.club/pref/fukushima/page/"
    ]
    file_name = "touhoku_"

elif area == "3":
    # 関東
    url = [
        "https://omairi.club/pref/ibaraki/page/",
        "https://omairi.club/pref/tochigi/page/",
        "https://omairi.club/pref/gunma/page/",
        "https://omairi.club/pref/saitama/page/",
        "https://omairi.club/pref/chiba/page/",
        "https://omairi.club/pref/tokyo/page/",
        "https://omairi.club/pref/kanagawa/page/"
    ]
    file_name = "kantou_"

elif area == "4":
    # 甲信越・北陸
    url = [
        "https://omairi.club/pref/niigata/page/",
        "https://omairi.club/pref/toyama/page/",
        "https://omairi.club/pref/ishikawa/page/",
        "https://omairi.club/pref/fukui/page/",
        "https://omairi.club/pref/yamanashi/page/",
        "https://omairi.club/pref/nagano/page/"
    ]
    file_name = "koushinetsu_"

elif area == "5":
    # 中部
    url = [
        "https://omairi.club/pref/gifu/page/",
        "https://omairi.club/pref/shizuoka/page/",
        "https://omairi.club/pref/aichi/page/",
        "https://omairi.club/pref/mie/page/"
    ]
    file_name = "hokkaidou_"

elif area == "6":
    # 近畿
    url = [
        "https://omairi.club/pref/shiga/page/",
        "https://omairi.club/pref/kyoto/page/",
        "https://omairi.club/pref/osaka/page/",
        "https://omairi.club/pref/hyogo/page/",
        "https://omairi.club/pref/nara/page/",
        "https://omairi.club/pref/wakayama/page/"
    ]
    file_name = "kinki_"

elif area == "7":
    # 中国
    url = [
        "https://omairi.club/pref/tottori/page/",
        "https://omairi.club/pref/shimane/page/",
        "https://omairi.club/pref/okayama/page/",
        "https://omairi.club/pref/hiroshima/page/",
        "https://omairi.club/pref/yamaguchi/page/"
    ]
    file_name = "chugoku_"

elif area == "8":
    # 四国
    url = [
        "https://omairi.club/pref/tokushima/page/",
        "https://omairi.club/pref/kagawa/page/",
        "https://omairi.club/pref/ehime/page/",
        "https://omairi.club/pref/kochi/page/"
    ]
    file_name = "shikoku_"

elif area == "9":
    # 九州
    url = [
        "https://omairi.club/pref/fukuoka/page/",
        "https://omairi.club/pref/saga/page/",
        "https://omairi.club/pref/nagasaki/page/",
        "https://omairi.club/pref/kumamoto/page/",
        "https://omairi.club/pref/oita/page/",
        "https://omairi.club/pref/miyazaki/page/",
        "https://omairi.club/pref/kagoshima/page/",
        "https://omairi.club/pref/okinawa/page/"
    ]
    file_name = "kyushuu_"

else:
    print("パラメータとして1～9を入力してください。")
    sys.exit()

base_data = []

detail_url_base = "https://omairi.club"

for pref_url in url:

    print(pref_url)

    i = 1

    while True:

        # URLを作成
        url_make = pref_url + str(i)

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

            target_flag = "その他"
            if target.find(class_="l_temple"):
                target_flag = "お寺"
            elif target.find(class_="l_shrine"):
                target_flag = "神社"

            name = target.find(class_='spot_name_body').text.replace(' ', '').strip()
            address = target.find(class_='spot_address').text.strip()

            detail_url = detail_url_base + target.find('a').get('href')

            res_detail = requests.get(detail_url)

            soup_page_detail = BeautifulSoup(res_detail.content, 'html.parser')

            ranking_ = soup_page_detail.html.find(class_="spot_ranking_info").find_all("span")[5].text

            ranking = int(ranking_[:len(ranking_) - 1])

#            print(ranking)

            ranking_data = [ranking, name, address, target_flag]

            base_data.append(ranking_data)

        i = i + 1

sort_data = sorted(base_data)


# データの箱を入れ替える
ranking = []
name = []
address = []
type = []

for data in sort_data:
    ranking.append(data[0])
    name.append(data[1])
    address.append(data[2])
    type.append(data[3])

# データ出力
max = 2000
max_count = int(len(ranking) / max) + 1

for count in range(max_count):

    print("count:" + str(count))

    start = count * max
    end = (count + 1) * max

    data_ranking = ranking[start:end]
    data_name = name[start:end]
    data_address = address[start:end]
    data_type = type[start:end]

    dic = {
        'ランキング': data_ranking,
        '名称': data_name,
        '住所': data_address,
        '神社・寺フラグ': data_type
    }

    df = pd.DataFrame(dic)

    #ファイル名
    with pd.ExcelWriter("./" + file_name + str(count) + ".xlsx", engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="sample_sheet", index=False)
