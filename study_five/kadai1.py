import eel
import csv

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code = item_code
        self.item_name = item_name
        self.price = price

    def get_price(self):
        return self.price

## オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list = []
        self.item_master = item_master
        self.item_count = 0
        self.item_sum_price = 0
        self.change = 0

    def add_item_order(self,item_code,quantity):
        self.item_order_list.append([item_code,quantity])

    def view_item_list(self):
        message = ""

        for master in self.item_master:
            for item in self.item_order_list:
                # 注文一覧の各コードをマスターと比較
                if master.item_code == item[0]:
                    message += f"商品コード:{item[0]}|価格:{master.price}|個数:{item[1]}\n"
                    self.item_count = self.item_count + int(item[1])
                    self.item_sum_price = self.item_sum_price + int(item[1]) * int(master.price)
        return message

    def exist_item_master(self,order_code):
        for item in self.item_master:
            if (item.item_code == order_code):
                return True
        return False

    def total_order(self,message):
        message += "\n#-------【合計】-------#"
        message += f"\n合計個数=>{self.item_count}個|合計金額=>{self.item_sum_price}"
        message += "\n#--------------------#"

        return message

    def check_payment(self,diposit):
        self.change = int(diposit) - self.item_sum_price

        if self.change < 0:
            return True
        return False

    def payment(self,message):
        message += f"\nお釣りの金額は{self.change}です"
        return message

def load_csv_master_file(master_csv):
    csv_file = open(master_csv,'r')
    master_list = csv.reader(csv_file)
    # ヘッダーをスキップする
    header = next(master_list)

    return master_list

@eel.expose
def order_confirm_to_python(order_confirm,payment):

    # アイテムマスタのファイル名
    master_csv = "item_master.csv"
    # マスターファイルを読み込み、マスターをリスト側で返却する
    item_list = load_csv_master_file(master_csv)

    item_master = []
    for item in item_list:
        item_master.append(Item(item[0],item[1],item[2]))

    # オーダーのインスタンスを作成し、アイテムマスターをセットする
    order = Order(item_master)

    for order_list in order_confirm:
        order_code = order_list['order_code']
        quantity = order_list['quantity']

        order.add_item_order(order_code,quantity)

    # オーダー表示
    message = order.view_item_list()
    # 合計金額表示
    message = order.total_order(message)
    # 支払金額をもとにお釣りを計算する
    isMinus = order.check_payment(payment)

    if isMinus == True:
        message += "\n金額が不足していますので、再度確認の上お支払いください"
    else:
        message = order.payment(message)

    eel.resultPaymentFromPython(message)

if __name__ == "__main__":
    eel.init("web")
    eel.start("html/index.html")
