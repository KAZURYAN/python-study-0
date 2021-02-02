import sys

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

    def add_item_order(self,item_code):
        self.item_order_list.append(item_code)

    def view_item_list(self):
        for master in self.item_master:
            for item in self.item_order_list:
                # 注文一覧の各コードをマスターと比較
                if master.item_code == item:
                    print(f"商品コード:{item}|価格:{master.price}")

    def exist_item_master(self,order_code):
        for master in self.item_master:
            if (master.item_code == order_code):
                return True

        return False

## メイン処理
def main():
    # アイテムマスタ準備
    item_master = []
    item_master.append(Item("001","りんご",100))
    item_master.append(Item("002","なし",200))
    item_master.append(Item("003","みかん",150))
    item_master.append(Item("004","パイナップル",950))

    # オーダー登録
    order=Order(item_master)

    while True:
        order_code = input("商品コードを入力してください（オーダーストップはend）=>")
        if (order_code == 'end'):
            print('注文を終わります')
            break

        if (order.exist_item_master(order_code) == False):
            print("マスタに存在しません、再度商品コードを入力してください")
            continue

        order.add_item_order(order_code)

    # オーダー表示
    order.view_item_list()

if __name__ == "__main__":
    main()