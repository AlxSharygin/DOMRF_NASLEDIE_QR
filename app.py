from flask import Flask, send_file, request
import qrcode
import os

app = Flask(__name__)

COUNTER_FILE = "counter.txt"

# Создаём файл счётчика, если его нет
if not os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, "w") as f:
        f.write("0")


def read_counter():
    """Читает текущее значение счётчика из файла"""
    try:
        with open(COUNTER_FILE, "r") as f:
            content = f.read().strip()
            return int(content) if content else 0
    except Exception:
        return 0


def write_counter(value):
    """Записывает новое значение счётчика в файл"""
    try:
        with open(COUNTER_FILE, "w") as f:
            f.write(str(value))
    except Exception as e:
        print(f"Ошибка записи счётчика: {e}")


@app.route('/')
def index():
    # Генерируем QR-код, ведущий на /track
    track_url = request.url_root + "track"
    qr = qrcode.make(track_url)
    qr_path = "qrcode.png"
    qr.save(qr_path)

    # Формируем HTML-страницу
    reset_url = request.url_root + "reset"
    current_count = read_counter()

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>QR Tracker</title>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; }}
            img {{ margin: 20px; border: 1px solid #ddd; border-radius: 8px; }}
            a {{ color: #007BFF; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <h1>📊 QR-код для отслеживания переходов</h1>
        <img src="/qrcode.png" alt="QR Code" width="250" />
        <p><strong>Текущее количество переходов: {current_count}</strong></p>
        <p><a href="{reset_url}">🔄 Сбросить счётчик</a></p>
        <p>Отсканируйте QR-код или перейдите вручную: <br>
           <a href="{track_url}">{track_url}</a></p>
    </body>
    </html>
    """


@app.route('/qrcode.png')
def serve_qr():
    """Отдаём сгенерированный QR-код как изображение"""
    return send_file("qrcode.png", mimetype='image/png')


@app.route('/track')
def track():
    """Увеличивает счётчик при переходе и показывает результат"""
    count = read_counter()
    count += 1
    write_counter(count)

    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>Переход зафиксирован</title><meta charset="utf-8"></head>
    <body style="text-align:center; padding:50px; font-family:Arial;">
        <h2>✅ Переход зафиксирован!</h2>
        <p><strong>Всего переходов: {count}</strong></p>
        <p><a href="/">← Вернуться на главную</a></p>
    </body>
    </html>
    """


@app.route('/reset')
def reset():
    """Сбрасывает счётчик в 0"""
    write_counter(0)
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Счётчик сброшен</title><meta charset="utf-8"></head>
    <body style="text-align:center; padding:50px; font-family:Arial;">
        <h2>🔄 Счётчик успешно сброшен!</h2>
        <p><a href="/">← Вернуться на главную</a></p>
    </body>
    </html>
    """


# ❗ ВАЖНО: НЕ РАСКОММЕНТИРОВЫВАТЬ app.run() — Railway использует Gunicorn/Waitress
# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port, debug=False)
