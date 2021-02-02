function checkSearchWord() {
    let searchWord = search_word.value;
    let csvName = csv_name.value;

    if (searchWord.trim().length == "" ){
        alert("検索ワードが入力されていません");
        return;
    }

    if (csvName.trim().length == "" ){
        alert("CSVファイルが入力されていません");
        return;
    }

    eel.searchKimetshChara(searchWord,csvName)
}

eel.expose(serachResultFromPython);
function serachResultFromPython(result) {
    showResult = document.getElementById("result_area").innerHTML + result
    document.getElementById("result_area").innerHTML = showResult + '\n';
}

// 入力したファイルが存在しない場合はアラートを表示する
eel.expose(errorFileNotFound);
function errorFileNotFound() {
    alert("ファイルが存在しません")
    return;
}