from flask import Flask, redirect, render_template_string
import os

app = Flask(__name__)

COUNTER_FILE = "counter.txt"

# Создаём файл счётчика, если его нет
if not os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, "w") as f:
        f.write("0")

@app.route('/')
def track_and_redirect():
    # Читаем текущее значение
    with open(COUNTER_FILE, "r") as f:
        count = int(f.read().strip())

    # Увеличиваем счётчик
    count += 1

    # Сохраняем новое значение
    with open(COUNTER_FILE, "w") as f:
        f.write(str(count))

    # Показываем страницу с информацией + кнопкой сброса
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>QR Счётчик</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    padding: 50px;
                    background-color: #f5f5f5;
                }
                .container {
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    display: inline-block;
                }
                h2 {
                    color: #333;
                }
                .count {
                    font-size: 2em;
                    font-weight: bold;
                    color: #007bff;
                    margin: 20px 0;
                }
                .btn {
                    display: inline-block;
                    padding: 10px 20px;
                    margin: 10px;
                    background-color: #dc3545;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                }
                .btn:hover {
                    background-color: #c82333;
                }
                .note {
                    color: #666;
                    font-size: 0.9em;
                    margin-top: 20px;
                }
            </style>
            <!-- Автоматический редирект через 5 секунд -->
            <meta http-equiv="refresh" content="5;url=https://xn--80aicbopm7a.xn--d1aqf.xn--p1ai/">
        </head>
        <body>
            <div class="container">
                <h2>✅ Спасибо за сканирование!</h2>
                <div class="count">Вы — {{ count }}-й посетитель</div>
                <p><a href="/reset" class="btn" onclick="return confirm('Сбросить счётчик на 0?')">🔄 Сбросить счётчик</a></p>
                <p class="note">Через 5 секунд вы автоматически перейдёте на сайт.</p>
            </div>
        </body>
        </html>
    ''', count=count)

@app.route('/reset')
def reset_counter():
    # Сбрасываем счётчик на 0
    with open(COUNTER_FILE, "w") as f:
        f.write("0")
    # Показываем сообщение об успехе и кнопку "назад"
    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Счётчик сброшен</title>
            <style>
                body { text-align: center; padding: 50px; font-family: Arial, sans-serif; }
                .success { color: green; font-size: 1.5em; }
                .btn { 
                    display: inline-block; 
                    padding: 10px 20px; 
                    background: #007bff; 
                    color: white; 
                    text-decoration: none; 
                    border-radius: 5px; 
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <div class="success">✅ Счётчик успешно сброшен на 0!</div>
            <p><a href="/" class="btn">← Вернуться на главную</a></p>
        </body>
        </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
