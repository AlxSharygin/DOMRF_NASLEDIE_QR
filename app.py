from flask import Flask, redirect
import os

app = Flask(__name__)

COUNTER_FILE = "counter.txt"

if not os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, "w") as f:
        f.write("0")

@app.route('/')
def track_and_redirect():
    with open(COUNTER_FILE, "r") as f:
        count = int(f.read().strip())

    count += 1

    with open(COUNTER_FILE, "w") as f:
        f.write(str(count))

    print(f"Сканирований: {count}")
    return redirect("https://xn--80aicbopm7a.xn--d1aqf.xn  --p1ai/", code=302)

# 🔁 Новый маршрут для сброса счётчика
@app.route('/reset')
def reset_counter():
    with open(COUNTER_FILE, "w") as f:
        f.write("0")
    return "<h2>✅ Счётчик успешно сброшен на 0!</h2><p><a href='/'>← Вернуться</a></p>"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
