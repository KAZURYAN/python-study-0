# 課題1
source = ["たんじろう","ぎゆう","ねずこ","むざん"]

def searchChara():
    charaName = input("鬼滅の登場人物の名前を入力してください:")

    if charaName in source:
        print('存在します')
    else:
        print('存在しませんので、リストに追加します')
        source.append(charaName)
        print(source)

if __name__ == "__main__":
    searchChara()