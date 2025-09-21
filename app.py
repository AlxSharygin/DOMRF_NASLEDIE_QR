from flask import Flask, send_file, request
import qrcode
import os

app = Flask(__name__)

COUNTER_FILE = "counter.txt"

# Убедимся, что файл существует
if not os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, "w") as f:
        f.write("0")

def read_counter():
    with open(COUNTER_FILE, "r") as f:
        return int(f.read().strip() or 0)

def write_counter(value):
    with open(COUNTER_FILE, "w") as f:
        f.write(str(value))

@app.route('/')
def index():
    # Генерируем QR-код, ведущий на /track
    track_url = request.url_root + "track"
    qr = qrcode.make(track_url)
    qr_path = "qrcode.png"
    qr.save(qr_path)

    # Возвращаем HTML с QR-кодом и ссылкой на сброс
    reset_url = request.url_root + "reset"
    return f"""
    <h1>QR-код для отслеживания переходов</h1>
    <img src="/qrcode.png" alt="QR Code" />
    <p>Текущее количество переходов: <strong>{read_counter()}</strong></p>
    <p><a href="{reset_url}">Сбросить счётчик</a></p>
    <p>Отсканируйте QR-код или перейдите по ссылке: <a href="{track_url}">{track_url}</a></p>
    """

@app.route('/qrcode.png')
def serve_qr():
    return send_file("qrcode.png", mimetype='image/png')

@app.route('/track')
def track():
    count = read_counter()
    count += 1
    write_counter(count)
    return f"""
    <h2>Переход зафиксирован!</h2>
    <p>Всего переходов: {count}</p>
    <p><a href="/">Вернуться</a></p>
    """

@app.route('/reset')
def reset():
    write_counter(0)
    return """
    <h2>Счётчик сброшен!</h2>
    <p><a href="/">Вернуться на главную</a></p>
    """

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
