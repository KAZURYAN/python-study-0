import os
import time
import datetime
import sys
import eel
import requests
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from jusho import Jusho

# 住所を取得
def fetch_address(elements):
    for address_elm in elements:
        in_post_address = address_elm.text
        if "〒" in in_post_address:
            position = in_post_address.find("〒")
            address = in_post_address[position+9:]
            return address
    return ""

# 電話番号を取得
def fetch_phone_number(element):
    phone_rules = re.compile(r"[\(]{0,1}[0-9]{2,4}[\)\-\(]{0,1}[0-9]{2,4}[\)\-]{0,1}[0-9]{3,4}")
    for string in element:
        is_phone = phone_rules.search(string.text)
        # 携帯電話番号か？
        if is_phone:
            return string.text
    return ""

# 郵便番号を取得
def fetch_post_address(elements):
    for address_elm in elements:
        in_post_address = address_elm.text
        if "〒" in in_post_address:
            position = in_post_address.find("〒")
            post_address = in_post_address[position+1:9]
            return post_address
    return ""

# 郵便番号から県を取得
def fetch_pref(post_address):
    jusho = Jusho()
    pref = jusho.from_postal_code(post_address)
    if len(pref.prefecture_kanji) != "0":
        return pref.prefecture_kanji
    else:
        return ""


# Chromeを起動する関数
def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)

def main():

    # Excelの読み込みを行う。欠損値NaNは削る。
    df = pd.read_excel("./抽出データ.xlsx", header=None, usecols=[0,1]).dropna(how='all').dropna(how='all', axis=1)
    # 1列目と2列目を半角スペースで結合する
    search_df = df[0] + ' ' + df[1]

    # 1件ずつ取りだし、配列に格納する
    search_maps = []
    for search_word in search_df:
        search_maps.append(search_word)

    google_maps_url = "https://www.google.co.jp/maps/?hl=ja"
    # driverを起動
    driver = webdriver.Chrome(ChromeDriverManager().install())

    # 検索ワードの数がある分、繰り返す
    for search_map in search_maps:
        # 指定したWebサイトを開く
        driver.get(google_maps_url)
        time.sleep(5)

        # 検索窓に入力
        driver.find_element_by_class_name("tactile-searchbox-input").send_keys(search_map)
        # 検索ボタンクリック
        driver.find_element_by_class_name("searchbox-searchbutton").click()
        time.sleep(5)

        # 検索結果を取得
        # section_results = driver.find_elements_by_class_name("section-result")
        cards = driver.find_elements_by_class_name("section-result-header-container")
        # 一覧画面のURLを取得
        current_url = driver.current_url

        # TODO 結果が取得できなかったらスキップする
        # 各検索結果単位で詳細情報を取得する
        while True:
            for i in range(len(cards)):
                print("")
                # １店舗の詳細画面の情報を取得
                card = driver.find_elements_by_class_name("section-result-title-container")
                # TODO エラーになるので広告帯ははあとで行う
                # # # 広告表示か否かを判定する
                # Ads = cards[i].find_elements_by_class_name("ad-badge")
                # # 最初のクラスがdisplay noneの場合は広告非表示、広告があるとTrueとなる
                # if Ads[0].is_displayed():
                #     continue
                # 詳細画面に移動する
                card[i].click()
                time.sleep(5)

                # elementをdriverにし、詳細画面のクラス名:店舗名を指定する
                title = driver.find_element_by_class_name("section-hero-header-title-title")
                address = fetch_address(driver.find_elements_by_class_name("ugiz4pqJLAG__primary-text"))
                post_address = fetch_post_address(driver.find_elements_by_class_name("ugiz4pqJLAG__primary-text"))
                phone = fetch_phone_number(driver.find_elements_by_class_name("ugiz4pqJLAG__primary-text"))
                pref = fetch_pref(post_address)
                print(i,title.text,phone,post_address,pref,address)
                # 検索一覧画面に戻る
                driver.get(current_url)
                time.sleep(3)

                # 次ページボタンが押下できるかを確認する
            is_exist_next_page = driver.find_element_by_id("n7lv7yjyC35__section-pagination-button-next").is_enabled()
            print(i,is_exist_next_page)

            if is_exist_next_page:
                time.sleep(5)
                driver.find_element_by_id("n7lv7yjyC35__section-pagination-button-next").click()
            else:
                break


if __name__ == "__main__":
    main()
