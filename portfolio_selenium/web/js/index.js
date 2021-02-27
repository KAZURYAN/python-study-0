$(function() {
    $('#contentSearch').popover({
        trigger: 'hover',
    });
});

function searchHomeschintai() {
    let search_keyword = $('#homesChintai').val();
    if (search_keyword == "") {
        alert("何も入力されていません");
        return;
    }
    // Pythonにアクセス
    eel.search_homes(search_keyword);
}