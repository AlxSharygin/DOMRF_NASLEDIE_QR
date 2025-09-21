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

@app.route('/')
def track_and_redirect():
    print("Запрос на / — увеличиваем счётчик")
    with lock:
        with open(COUNTER_FILE, "r") as f:
            count = int(f.read().strip())

        count += 1

        with open(COUNTER_FILE, "w") as f:
            f.write(str(count))

    print(f"Сканирований: {count}")
    return redirect("https://xn--80aicbopm7a.xn--d1aqf.xn--p1ai/", code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
