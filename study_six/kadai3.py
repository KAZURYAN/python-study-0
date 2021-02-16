import requests
import configparser
import sys
import json
import pandas as pd

# アプリIDを取得する
def read_product_key():
    config = configparser.ConfigParser()
    config.read('apikey.conf')
    key_name = 'API_KEY_PRODUCT'
    return config.get(key_name, 'key')

# パラメータを付随する
def make_product_url(api_key, genre_id):
    search_params = {
        "format" :  "json",
        "genreId" : genre_id,
        "applicationId" : api_key
    }
    return search_params

def main():
    base_url = 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?'

    genre_id = input("ジャンルIDを入力してください:")
    if (genre_id == ""):
        print("ジャンルIDが入力されませんでした")
        exit()

    api_key = read_product_key()
    params = make_product_url(api_key, genre_id)

    response = requests.get(base_url, params)
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