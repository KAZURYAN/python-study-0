import os
import time
import sys
from selenium.webdriver import Chrome, ChromeOptions
from pprint import pprint
# import pandas as pd

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

# 会社名を取得して、webelement形式で返却する
def fetch_company_name_list(driver):
    class_name = "cassetteRecruit__name"
    return driver.find_elements_by_class_name(class_name)

# 求人のキャッチコピーを取得して、webelement形式で返却する
def fetch_copy_list(driver):
    class_name = "cassetteRecruit__copy"
    return driver.find_elements_by_class_name(class_name)

# 指定したテーブルのエレメントを取得
def fetch_table_elm(driver,table_name):
    return driver.find_elements_by_class_name("tableCondition")

# 給与のリストを取得
def fetch_pay_list(driver,table_elm):
    exp_pay_list = []
    exp_table_list = []

    # tdタグの3番目が給与に該当する
    for elm in table_elm:
        exp_table_list = elm.find_elements_by_tag_name("td")
        exp_pay_list.append(exp_table_list[3].text)

    return exp_pay_list

# main処理
def main():
    search_keyword = "高収入"

    driver = webdriver.Chrome(ChromeDriverManager().install())

    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)

    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass

    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    # 会社名リスト
    exp_name_list = []
    # キャッチコピーリスト
    exp_copy_list = []
    # 給与リスト
    exp_pay_list = []
    # 検索した一覧結果の会社名を取得
    exp_name_list = fetch_company_name_list(driver)
    # 求人キャッチコピーの取得
    exp_copy_list = fetch_copy_list(driver)
    # 給与の取得
    table_name = "tableCondition"
    # tableのtdに給与が含まれている為、テーブルのエレメントを取得する
    table_elm = fetch_table_elm(driver,table_name)
    # テーブルのエレメントから給与だけのリストを取得する
    exp_pay_list = fetch_pay_list(driver,table_elm)

    # 会社名,求人キャッチコピー、給与の出力
    for name,copy,pay in zip(exp_name_list,exp_copy_list,exp_pay_list):
        print(name.text,copy.text,pay)

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()