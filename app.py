from flask import Flask, redirect, request, render_template_string
import os

app = Flask(__name__)

COUNTER_FILE = "counter.txt"

# Инициализация файла счётчика
def init_counter():
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f:
            f.write("0")
    else:
        try:
            with open(COUNTER_FILE, "r") as f:
                content = f.read().strip()
                int(content)
        except (ValueError, OSError):
            with open(COUNTER_FILE, "w") as f:
                f.write("0")

init_counter()


# 🚀 Главная страница — увеличивает счётчик и сразу редиректит (НИКАКОГО HTML!)
@app.route('/')
def track_and_redirect():
    try:
        with open(COUNTER_FILE, "r") as f:
            count = int(f.read().strip())
    except (ValueError, OSError):
        count = 0

    count += 1

    try:
        with open(COUNTER_FILE, "w") as f:
            f.write(str(count))
    except OSError:
        pass

    print(f"Сканирований: {count}")
    return redirect("https://xn--80aicbopm7a.xn--d1aqf.xn--p1ai/", code=302)


# ⚙️ Страница настроек — НИКОГДА не увеличивает счётчик
@app.route('/settings', methods=['GET', 'POST'])
def settings_counter():
    if request.method == 'POST':
        try:
            with open(COUNTER_FILE, "w") as f:
                f.write("0")
        except OSError:
            pass
        return redirect("/settings", code=302)  # ← предотвращает +1 после сброса

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
        <p>✅ После сброса страница обновится автоматически.</p>
    </body>
    </html>
    """
    return render_template_string(html)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
