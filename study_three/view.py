import csv
import eel
import numpy as np

@eel.expose
def searchKimetshChara(searchWord,csvName):
    resultStr = ""

    try:
        source = csvLoad(csvName)

        if searchWord in source:
            resultStr = f'「{searchWord}はあります」'

            eel.serachResultFromPython(resultStr)
        else:
            resultStr = f'「{searchWord}はいません」\n'
            resultStr += f'「{searchWord}を追加します」'
            source.append(searchWord)
            writeCharaForCsv(source,csvName)

            eel.serachResultFromPython(resultStr)

    except FileNotFoundError as error:
        eel.errorFileNotFound()

# CSVを読み込みリスト型にして返却
def csvLoad(csvName):
    with open(f'./web/csv/{csvName}') as filekimetsuchara:
        reader = csv.reader(filekimetsuchara)
        for source in reader:
            pass

        return source

# 入力したキャラクターが存在しない場合はCSVに追加
def writeCharaForCsv(source,csvName):
    with open(f'./web/csv/{csvName}', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(source)

if __name__ == "__main__":
    eel.init("web")
    eel.start("html/index.html")