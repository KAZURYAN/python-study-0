# 課題1
def kadai1():
    name1:str = 'ねずこ'
    name2:str = 'ぜんいつ'
    print(f'「{name1}」と「{name2}」は仲間です')

# 課題2
def kadai2():
    # name1:str = 'ねずこ'
    name2:str = 'むざん'

    if name2 == 'むざん':
        print('仲間ではありません')

# 課題3
def kadai3():
    name = ["たんじろう","ぎゆう","ねずこ","むざん"]
    name.append("ぜんいつ")

    print(name)


# 課題4
def kadai4():
    name = ["たんじろう","ぎゆう","ねずこ","むざん"]
    name.append("ぜんいつ")

    for str in name:
        print(str)


kadai1()
kadai2()
kadai3()
kadai4()