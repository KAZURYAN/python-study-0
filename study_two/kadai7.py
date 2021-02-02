import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import datetime
import sys
import pandas as pd

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

# driver起動処理
def openChromeDriver():
    """chromedriver起動

    Returns:
        driver: driverを返却
    """
    if os.name == 'nt': #Windows
        return set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        return set_driver("chromedriver", False)

# 会社名を取得して、webelement形式で返却する
def fetch_company_name_list(driver):
    class_name = "cassetteRecruit__name"
    return driver.find_elements_by_class_name(class_name)

# 求人のキャッチコピーを取得して、webelement形式で返却する
def fetch_copy_list(driver):
    class_name = "cassetteRecruit__copy"
    return driver.find_elements_by_class_name(class_name)

# 募集区分を取得して、webElement形式で返却する
def fetch_emp_status_list(driver):
    class_name = "labelEmploymentStatus"
    return driver.find_elements_by_class_name(class_name)

# ログ出力の開始
def start_logging():
    # 現在時刻を取得
    str_now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    return open(f'log_file_{str_now}.txt','a')

# ログ出力の終了
def close_logging(log_file):
    log_file.close()

# エラーログを出力する
def write_error_log(log_file,error):
    log_file.write('error catched. start------' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '------\n')
    log_file.write(str(error))
    log_file.write(str(type(error)))
    log_file.write('\nend------\n')

# main処理
def main():
    # ログの取得開始
    log_file = start_logging()

    target_url = "https://tenshoku.mynavi.jp/"
    search_keyword = input("検索キーワードを入力してください=>")

    log_file.write(f'検索キーワードを入力してください=>{search_keyword}\n')

    # driverを起動
    driver = openChromeDriver()

    # Webサイトを開く
    driver.get(target_url)
    time.sleep(5)

    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except Exception as error:
        write_error_log(log_file,error)

    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    # ページ終了まで繰り返し取得する
    name_list = []
    copy_list = []
    rectype_list = []
    search_result_list = []

    fetch_company_count = 1
    page_count = 0

    # 検索結果のページャーがあれば、遷移して次ページの結果を取得
    while True:
        try:
            # 検索した一覧結果の会社名を取得
            exp_name_list = fetch_company_name_list(driver)
            # 求人キャッチコピーの取得
            exp_copy_list = fetch_copy_list(driver)
            # 募集区分の取得
            exp_rectype_list = fetch_emp_status_list(driver)

            # 1ページ分をリスト追加、2ページ目以降があればリストに追記
            for name,copy,rectype in zip(exp_name_list,exp_copy_list,exp_rectype_list):
                name_list.append(name.text)
                copy_list.append(copy.text)
                rectype_list.append(rectype.text)
                log_file.write(f'現在{fetch_company_count}件処理中です\n')
                fetch_company_count += 1

        except Exception as error:
            write_error_log(log_file,error)

        # 次ページがあれば、遷移する
        try:
            if len(driver.find_elements_by_class_name("iconFont--arrowLeft")) > 0:
                # 次ページのURL(href)を取得
                next_page = driver.find_element_by_class_name("iconFont--arrowLeft").get_attribute("href")
                # 指定したWebページを開く
                log_file.write('次ページへ遷移します\n')
                driver.get(next_page)
                page_count = page_count + 1
                time.sleep(10)

            # 次ページがないため、終了する
            else:
                break

        except Exception as error:
            write_error_log(log_file,error)

    log_file.write(f'遷移したページ数は全部で{page_count}ページです\n')

    # 取得結果をCSVへ追記するためのリストへ追記する
    for name,copy,rectype in zip(name_list,copy_list,rectype_list):
        search_result_list.append([name,copy,rectype])

    # CSVへ出力する
    df = pd.DataFrame(search_result_list)
    df.to_csv(f"{search_keyword}_list.csv", header=None, index=False)

    # ログの取得終了
    close_logging(log_file)

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()