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

    # 商品コードと価格の表示を実行する
    def view_item_list(self):
        for master in self.item_master:
            for item in self.item_order_list:
                if master.item_code == item:
                    print(f"商品コード:{item}|価格:{master.price}")


## メイン処理
def main():
    # アイテムマスタ準備
    item_master = []
    item_master.append(Item("001","りんご",100))
    item_master.append(Item("002","なし",200))
    item_master.append(Item("003","みかん",150))

    # オーダー登録
    order=Order(item_master)
    order.add_item_order("001")
    order.add_item_order("002")
    order.add_item_order("003")

    # オーダー表示
    order.view_item_list()

if __name__ == "__main__":
    main()