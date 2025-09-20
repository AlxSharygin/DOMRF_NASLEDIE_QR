from flask import Flask, redirect, request, render_template_string
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
    return redirect("https://xn--80aicbopm7a.xn--d1aqf.xn--p1ai/", code=302)


# 🔁 Страница сброса: показывает счётчик и кнопку сброса
@app.route('/settings', methods=['GET', 'POST'])
def settings_counter():
    if request.method == 'POST':
        # Сбрасываем счётчик только при POST-запросе (нажатии кнопки)
        with open(COUNTER_FILE, "w") as f:
            f.write("0")
        message = "✅ Счётчик успешно сброшен на 0!"
    else:
        message = ""

    # Читаем текущее значение счётчика для отображения
    with open(COUNTER_FILE, "r") as f:
        count = int(f.read().strip())

    # HTML-страница с формой и отображением счётчика
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Сброс счётчика</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h2>🔁 Страница сброса счётчика</h2>
        <p><strong>Текущее количество переходов по QR-коду: {count}</strong></p>
        <form method="POST">
            <button type="submit">🔄 Сбросить счётчик</button>
        </form>
        <p><a href="/">← Вернуться на главную</a></p>
        {"<p style='color: green;'>" + message + "</p>" if message else ""}
    </body>
    </html>
    """
    return render_template_string(html)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
