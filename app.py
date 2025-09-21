from flask import Flask, redirect, request, make_response
import os
import threading

app = Flask(__name__)
COUNTER_FILE = os.path.join(os.path.dirname(__file__), "counter.txt")
lock = threading.Lock()

@app.route('/health')
def health_check():
    return "OK", 200

@app.route('/run')
def track_and_redirect():
    response = make_response(redirect("https://xn--80aicbopm7a.xn--d1aqf.xn--p1ai/", code=302))

    if request.cookies.get('visited') == 'true':
        print("Уже посещали — не увеличиваем счётчик")
        return response

    with lock:
        if os.path.exists(COUNTER_FILE):
            with open(COUNTER_FILE, "r") as f:
                count = int(f.read().strip())
        else:
            count = 0

        count += 1

        with open(COUNTER_FILE, "w") as f:
            f.write(str(count))

    print(f"Сканирований: {count}")
    response.set_cookie('visited', 'true', max_age=3600)  # 1 час
    return response

@app.route('/reset')
def reset_counter():
    with lock:
        with open(COUNTER_FILE, "w") as f:
            f.write("0")
    print("Счетчик сброшен")
    return "<h2>✅ Счётчик успешно сброшен на 0!</h2><p><a href='/run'>← Вернуться</a></p>"
