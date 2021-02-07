import csv
import datetime

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

    def view_item_list(self,log_file):
        for master in self.item_master:
            for item in self.item_order_list:
                # 注文一覧の各コードをマスターと比較
                if master.item_code == item[0]:
                    print(f"商品コード:{item[0]}|価格:{master.price}|個数:{item[1]}")
                    log_file.write(f"商品コード:{item[0]}|価格:{master.price}|個数:{item[1]}\n")
                    self.item_count = self.item_count + int(item[1])
                    self.item_sum_price = self.item_sum_price + int(item[1]) * int(master.price)


    def exist_item_master(self,order_code):
        for item in self.item_master:
            if (item.item_code == order_code):
                return True

        return False

    def total_order(self,log_file):
        print("\n#--------------#")
        log_file.write(f"#--------------#\n")
        print(f"個数=>{self.item_count}|合計金額=>{self.item_sum_price}")
        log_file.write(f"個数=>{self.item_count}|合計金額=>{self.item_sum_price}\n")
        print("#--------------#")
        log_file.write(f"#--------------#\n")

    def check_payment(self,diposit):
        self.change = int(diposit) - self.item_sum_price

        if self.change < 0:
            return True
        return False

    def payment(self,log_file):
        print(f"お釣りの金額は{self.change}です")
        log_file.write(f"お釣りの金額は{self.change}です\n")

class Logging:
    # ログ出力の開始
    def start_logging(self):
        str_now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        return open(f'log_file_{str_now}.txt','a')

    # ログ出力の終了
    def close_logging(self,log_file):
        log_file.close()

## メイン処理
def main():

    # アイテムマスタ
    master_csv = "item_master.csv"
    csv_file = open(master_csv, 'r')
    # CSVデータを読み込む
    item_list = csv.reader(csv_file)
    # ヘッダーをスキップする
    header = next(item_list)

    item_master = []
    for item in item_list:
        item_master.append(Item(item[0],item[1],item[2]))

    # オーダーのインスタンス作成し、アイテムマスターをセットする
    order = Order(item_master)

    order_code = ""
    quantity = 0

    # ログの開始
    log = Logging()
    log_file = log.start_logging()

    while True:
        order_code = input("商品コードを入力してください（オーダーストップはend）=>")
        log_file.write(f"商品コードを入力してください（オーダーストップはend）=>{order_code}\n")
        if (order_code == 'end'):
            print('注文を終わります')
            log_file.write("注文を終わります")
            break

        quantity = input("個数を入力してください=>")
        log_file.write(f"個数を入力してください=>{quantity}\n")

        if (order.exist_item_master(order_code) == False):
            print("マスタに存在しません、再度商品コードを入力してください")
            log_file.write(f"マスタに存在しません、再度商品コードを入力してください{order_code}\n")
            continue

        order.add_item_order(order_code,quantity)

    # オーダー表示
    order.view_item_list(log_file)

    # 合計金額表示
    order.total_order(log_file)

    while True:
        # 支払金額を入力
        diposit = input("支払金額を入力してください=>")
        log_file.write(f"支払金額を入力してください=>{diposit}\n")
        isMinus = order.check_payment(diposit)

        if isMinus == True:
            print("金額が不足していますので、再度お支払いください")
            log_file.write(f"金額が不足していますので、再度お支払いください\n")
            continue
        else:
            order.payment(log_file)
            break

    log.close_logging(log_file)

if __name__ == "__main__":
    main()