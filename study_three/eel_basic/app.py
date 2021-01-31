import eel
import time
import ntplib
import datetime
from time import ctime

# 以下@のデコレーターえ、JSから本関数にアクセス出来るようになる
@eel.expose
def ask_python_from_js_get_time(server):
    now_time = ""
    try:
        ntp_client = ntplib.NTPClient()
        ntp_resp = ntp_client.request(server)
        ntp_time = datetime.datetime.strptime(ctime(ntp_resp.tx_time), "%a %b %d %H:%M:%S %Y")
        now_time = ntp_time.strftime("%Y/%m/%d %H:%M:%S")
    except Exception as e:
        print(e)
        now_time = "Woops! something went wrong."
    finally:
        # JS側に現在時刻を返却する
        eel.run_js_from_python(now_time)

# ウェブコンテンツを持つフォルダー
eel.init("web")

# 最初に表示するhtmlページ
# eel.start("html/index.html")
eel.start("html/index.html", port=8080, size=(1200, 700))