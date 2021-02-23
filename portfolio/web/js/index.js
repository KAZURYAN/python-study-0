$(function() {
    $('#contentSearch').popover({
        trigger: 'hover',
    });
});

function searchRakutenProduct() {
    let searchProduct = $('#rakutenProduct').val();
    if (searchProduct == "") {
        alert("何も入力されていません");
        return;
    }
    // Pythonにアクセス
    eel.search_rakuten_product(searchProduct);
}