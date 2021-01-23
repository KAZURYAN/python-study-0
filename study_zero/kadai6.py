# 課題6

def existChara(charaName):
    name = ["たんじろう","ぎゆう","ねずこ","むざん"]

    if charaName in name:
        print('{}は仲間です'.format(charaName))
    else:
        print('{}は仲間では有りません'.format(charaName))

existChara('いのすけ')