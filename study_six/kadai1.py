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
def make_product_url(api_key, keyword):
    search_params = {
        "format" :  "json",
        "keyword" : keyword,
        "applicationId" : api_key
    }
    return search_params

def main():
    base_url = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?'

    keyword = input("検索キーワードを入力してください:")
    api_key = read_product_key()
    params = make_product_url(api_key, keyword)

    # 楽天APIを実行する
    response = requests.get(base_url, params)
    items = response.json()

    for item in items['Items']:
        product = item['Item']
        print(product['itemName'] + '|' + (str)(product['itemPrice']) + '円')

if __name__ == ('__main__'):
    main()