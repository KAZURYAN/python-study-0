import requests
import configparser
import sys
import json
import pandas as pd
import os
from os.path import join, dirname
from dotenv import load_dotenv
from request_rakuten_rank_api import RequestRakutenRankAPI

def read_api_key():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    return os.environ.get("API_KEY")

def main():
    # 商品ランキングを取得する楽天APIのURL
    base_url = 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?'

    genre_id = input("ジャンルIDを入力してください:")
    if (genre_id == ""):
        print("ジャンルIDが入力されませんでしたので終了します")
        exit()

    api_key = read_api_key()
    rankApi = RequestRakutenRankAPI(base_url, api_key, genre_id)

    params = rankApi.make_url()
    # 楽天API実行
    response = rankApi.execute_api(params)
    is_success = rankApi.success(response.status_code)

    if (is_success == False):
        print('APIの取得に失敗していますので処理を終了します')
        exit()

    # Json形式に変換します
    items = response.json()
    index_key = ['rank','itemName','itemPrice','genreId']
    item_list = []

    for i in range(0, len(items['Items'])):
        temp_item = {}
        item = items['Items'][i]['Item']
        for key, value in item.items():
            if key in index_key:
                temp_item[key] = value
        item_list.append(temp_item.copy())

    items_df = pd.DataFrame(item_list)
    items_df = items_df.reindex(columns=['rank','itemName','itemPrice','genreId'])
    items_df.columns = ['順位','商品名','価格','ジャンルID']

    items_df.to_csv('./rakuten_product_runk.csv')

if __name__ == ('__main__'):
    main()