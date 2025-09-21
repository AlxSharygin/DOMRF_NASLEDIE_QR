from flask import Flask, redirect
import os
import threading

app = Flask(__name__)
COUNTER_FILE = "counter.txt"
lock = threading.Lock()

if not os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, "w") as f:
        f.write("0")

@app.route('/health')
def health_check():
    return "OK", 200

@app.route('/')
def track_and_redirect():
    with lock:
        with open(COUNTER_FILE, "r") as f:
            count = int(f.read().strip())

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
    print(f"Сканирований: {count}")
    return "<h2>✅ Счётчик успешно сброшен на 0!</h2><p><a href='/'>← Вернуться</a></p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
