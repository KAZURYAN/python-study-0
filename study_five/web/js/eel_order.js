function plusRow() {
    const $table = $('.js-order-table');
    let $tr = $('<tr></tr>');
    // 商品コード
    let $tdOrderCode = $('<td></td>', {
    }).append(
        $('<input>', {
            class: 'order_code',
            name: 'order_code',
            type: 'text',
        })
    );
    // 個数
    let $tdQuantity = $('<td></td>', {
    }).append(
        $('<input>', {
            class: 'quantity',
            name: 'quantity',
            type: 'text',
        })
    );
    // 追加ボタン
    let $tdAddbutton = $('<td></td>', {
    }).append(
        $('<button>', {
            text: '+',
            onClick: "plusRow()"
        })
    );

    $tr.append($tdOrderCode);
    $tr.append($tdQuantity);
    $tr.append($tdAddbutton);

    // テーブルの真下に一行追加する
    $table.append($tr);
}

// Python側に注文の確認を問い合わせる
function order() {
    let order_confirm = [];
    let payment = $('#payment').val();
    const $table = $('.js-order-table tr');

    $.each($table, function(i,tr) {
        // ヘッダーはスキップする
        if (i == 0) {
            return true;
        }
        let $tr = $(tr);
        let orderCode = $tr.find('.order_code').val();
        let quantity = $tr.find('.quantity').val();

        let rowData = {
            'order_code': orderCode,
            'quantity': quantity,
        }
        // order[i] = rowData;
        order_confirm.push(rowData);

    });

    // Pythonにアクセス
    eel.order_confirm_to_python(order_confirm,Number(payment))
}

eel.expose(resultPaymentFromPython)
function resultPaymentFromPython(message) {
    document.getElementById("result_area").innerHTML = ""
    document.getElementById("result_area").innerHTML = message;
}