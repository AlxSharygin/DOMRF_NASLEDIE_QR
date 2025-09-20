from flask import Flask, redirect, request, render_template_string
import os

app = Flask(__name__)

COUNTER_FILE = "counter.txt"

# Инициализация файла, если его нет или он повреждён
def init_counter():
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f:
            f.write("0")
    else:
        try:
            with open(COUNTER_FILE, "r") as f:
                content = f.read().strip()
                int(content)  # Проверяем, что можно преобразовать в число
        except (ValueError, OSError):
            # Если файл повреждён — пересоздаём
            with open(COUNTER_FILE, "w") as f:
                f.write("0")

# Вызываем инициализацию при старте
init_counter()


@app.route('/')
def track_and_redirect():
    try:
        with open(COUNTER_FILE, "r") as f:
            count = int(f.read().strip())
    except (ValueError, OSError):
        count = 0  # Если ошибка — начинаем с нуля

    count += 1

    try:
        with open(COUNTER_FILE, "w") as f:
            f.write(str(count))
    except OSError:
        pass  # Игнорируем ошибки записи (можно логировать при необходимости)

    print(f"Сканирований: {count}")
    return redirect("https://xn--80aicbopm7a.xn--d1aqf.xn--p1ai/", code=302)


@app.route('/settings', methods=['GET', 'POST'])
def settings_counter():
    if request.method == 'POST':
        try:
            with open(COUNTER_FILE, "w") as f:
                f.write("0")
            message = "✅ Счётчик успешно сброшен на 0!"
        except OSError:
            message = "❌ Ошибка при сбросе счётчика"
    else:
        message = ""

    try:
        with open(COUNTER_FILE, "r") as f:
            count = int(f.read().strip())
    except (ValueError, OSError):
        count = 0

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
    port = int(os.environ.get('PORT', 8080))  # ← Обратите внимание: теперь 8080, как в логе
    app.run(host='0.0.0.0', port=port)
