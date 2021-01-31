function getCurrentTime() {
    let server = document.getElementById("ntp").value;

    if (server.trim().length == 0) {
        document.getElementById("result").innerHTML = "Enter NTP server address!";
        return;
    }

    // app.pyのデコレーターを起動
    eel.ask_python_from_js_get_time(server);
}

// 本exposeで、pythonから本関数を呼べるようにする
eel.expose(run_js_from_python);
function run_js_from_python(msg) {
    document.getElementById("result").innerHTML = msg;
}