# 課題4
import csv

def csvLoad():
    with open('study_one/kimetsuchara.csv') as filekimetsuchara:
        reader = csv.reader(filekimetsuchara)

        for source in reader:
            pass

        return source

def searchChara(source):
    charaName = input("鬼滅の登場人物の名前を入力してください:")

    if charaName in source:
        print('存在します')
    else:
        print('存在しませんので、リストに追加します')
        source.append(charaName)
        writeCharaForCsv(source)

def writeCharaForCsv(source):
    with open('study_one/kimetsucharaAppend.csv ', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(source)

if __name__ == "__main__":
    source = csvLoad()
    searchChara(source)
