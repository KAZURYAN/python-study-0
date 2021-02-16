import requests
import configparser
import sys
import json

# アプリIDを取得する
def read_product_key():
    config = configparser.ConfigParser()
    config.read('apikey.conf')
    key_name = 'API_KEY_PRODUCT'
    return config.get(key_name, 'key')

# パラメータを付随する
def make_product_url(api_key, keyword, genreId):
    search_params = {
        "format" :  "json",
        "keyword" : keyword,
        "applicationId" : api_key
    }
    return search_params

# キーワードとジャンルID両方未入力かを確認する
def check_api_request_param_is_none(keyword, genreId):
    if (keyword == "" and genreId == ""):
        return True
    return False

def main():
    base_url = 'https://app.rakuten.co.jp/services/api/Product/Search/20170426?'

    keyword = input("検索キーワードを入力してください:")
    genreId = input('ジャンルIDを入力してください:')

    if (check_api_request_param_is_none(keyword, genreId) == True):
        print("キーワード、ジャンルIDが入力されませんでした")
        exit()

    api_key = read_product_key()
    params = make_product_url(api_key, keyword, genreId)
    # 楽天APIを実行する
    response = requests.get(base_url, params)
    items = response.json()

    for item in items['Products']:
        product = item['Product']
        print(f'商品名:{product["productName"]} | 購入可能な最低価格:{(str)(product["salesMinPrice"])} | 購入可能な最高価格:{(str)(product["salesMaxPrice"])}')

if __name__ == ('__main__'):
    main()