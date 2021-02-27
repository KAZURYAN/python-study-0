import os
import time
import datetime
import sys
import eel
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

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

# main処理
@eel.expose
def search_homes(search_keyword):
    print(search_keyword)
    target_url = "https://www.homes.co.jp/chintai/"

    # driverを起動
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(5)

    # Webサイトを開く
    driver.get(target_url)
    time.sleep(5)

    # 検索窓に入力
    driver.find_element_by_class_name("inputTxt").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("btnSubmit").click()

    # 各取得値保存リストの定義
    address_list = []
    traffic_list = []
    age_list = []

    # 検索結果のページャーがあれば、遷移して次ページの結果を取得
    while True:
        # 検索一覧の集合体class名:bukkenSpecを取得
        elements_bukkenspec = driver.find_elements_by_class_name("bukkenSpec")

        for bukken_spec in elements_bukkenspec:
            # bukkenSpec内をtbody単位で取得
            element_tbody_tags = bukken_spec.find_elements(By.TAG_NAME,"tbody")

            # tbody単位でforを実施
            for element_tbody in element_tbody_tags:
                # tbody内部にあるtrタグを取得する
                element_tr_tags = element_tbody.find_elements(By.TAG_NAME,"tr")

                exist_address = False
                exist_traffic = False
                exist_age = False

                for element_tr_tag in element_tr_tags:
                    # ヘッダーを取得
                    element_th_tag = element_tr_tag.find_element(By.TAG_NAME, "th")

                    if element_th_tag.text == "所在地":
                        element_td_tag = element_tr_tag.find_element(By.TAG_NAME, "td")
                        address_list.append(element_td_tag.text)
                        exist_address = True
                        continue

                    if element_th_tag.text == "交通":
                        element_td_tag = element_tr_tag.find_element(By.TAG_NAME, "td")
                        traffic_list.append(element_td_tag.text.replace('\n',''))
                        exist_traffic = True
                        continue

                    if element_th_tag.text == "築年数/階数":
                        element_td_tag = element_tr_tag.find_element(By.TAG_NAME, "td")
                        age_list.append(element_td_tag.text)
                        exist_age = True
                        continue

                # tbodyタグ内部の繰り返し処理すべて実施後に、以下の判定を行う。
                # 所在地がない場合はリストに空白を入れる
                if exist_address == False:
                    address_list.append("")

                # 交通がない場合はリストに空白を入れる
                if exist_traffic == False:
                    traffic_list.append("")

                # 築年数/階数がない場合はリストに空白を入れる
                if exist_age == False:
                    age_list.append("")

        # 次ページがあれば、遷移する
        if len(driver.find_elements_by_class_name("nextPage")) > 0:
            time.sleep(5)
            driver.find_element_by_css_selector("li.nextPage > a").click()

       # 次ページがないため、終了する
        else:
            break

    search_result_list = []

    # 取得結果をCSVへ追記するためのリストへ追記する
    for address,traffic,age in zip(address_list,traffic_list,age_list):
        search_result_list.append([address,traffic,age])

    # CSVへ出力する
    df = pd.DataFrame(search_result_list)
    df.to_csv(f"{search_keyword}_list.csv", header=None, index=False)

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    eel.init("web")
    eel.start("html/index.html")