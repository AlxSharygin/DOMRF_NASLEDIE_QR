import os
import threading
from flask import Flask, redirect

app = Flask(__name__)
COUNTER_FILE = os.path.join(os.path.dirname(__file__), "counter.txt")  # ← Абсолютный путь
lock = threading.Lock()

# УДАЛИ БЛОК ПРОВЕРКИ ПРИ ЗАПУСКЕ — он больше не нужен

@app.route('/health')
def health_check():
    return "OK", 200

@app.route('/run')
def track_and_redirect():
    with lock:
        # Читаем текущее значение или начинаем с 0
        if os.path.exists(COUNTER_FILE):
            with open(COUNTER_FILE, "r") as f:
                count = int(f.read().strip())
        else:
            count = 0

        count += 1

        with open(COUNTER_FILE, "w") as f:
            f.write(str(count))

    print(f"Сканирований: {count}")
    return redirect("https://xn--80aicbopm7a.xn--d1aqf.xn--p1ai/", code=302)

@app.route('/reset')
def reset_counter():
    with lock:
        with open(COUNTER_FILE, "w") as f:
            f.write("0")
    print("Счетчик сброшен")
    return "<h2>✅ Счётчик успешно сброшен на 0!</h2><p><a href='/run'>← Вернуться</a></p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)  # ← Отключи debug для сохранения состояния
