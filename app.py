from flask import Flask, redirect

app = Flask(__name__)

# Счётчик
clicks = 0

@app.route('/')
def track_and_redirect():
    global clicks
    clicks += 1
    print(f"Сканирований: {clicks}")  # или сохраните в файл/БД
    # Перенаправляем на целевой сайт
    return redirect("https://xn--80aicbopm7a.xn--d1aqf.xn--p1ai/", code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
