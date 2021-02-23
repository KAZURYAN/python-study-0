import eel
import requests
import configparser
import json
import sys
import os
import pandas as pd
from dotenv import load_dotenv
from os.path import join, dirname
from request_rakuten_product_api import RequestRakutenProductAPI

# アプリIDを取得する
def read_product_key():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    return os.environ.get("API_KEY")

@eel.expose
def search_rakuten_product(search_product):
    # print(type(search_product))
    # sys.exit()
    base_url = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?'

    api_key = read_product_key()
    product = RequestRakutenProductAPI(base_url, api_key, search_product)

    # APIパラメータを作成する
    params = product.make_url()

    # 楽天APIを実行する
    response = product.execute_api(params)
    items = response.json()
    item_list = []

    for i in range(0,len(items['Items'])):
        item = items['Items'][i]['Item']
        item_list.append([item['itemName'],item['itemPrice']])

    items_df = pd.DataFrame(item_list)
    items_df.columns = ['商品名','価格']

    items_df.to_csv('./rakuten_product.csv')

if __name__ == "__main__":
    eel.init("web")
    eel.start("html/index.html")