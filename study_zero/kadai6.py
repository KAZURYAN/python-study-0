# 課題6

def existChara(charaName):
    name = ["たんじろう","ぎゆう","ねずこ","むざん"]

    if charaName in name:
        print(f'{charaName}は仲間です')
    else:
        print(f'{charaName}は仲間では有りません')

existChara('いのすけ')