from flask import Flask, redirect
import os

app = Flask(__name__)

COUNTER_FILE = "counter.txt"

# Создаём файл, если его нет
if not os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, "w") as f:
        f.write("0")

@app.route('/')
def track_and_redirect():
    count = 0

    # Читаем счётчик с обработкой ошибок
    try:
        with open(COUNTER_FILE, "r") as f:
            content = f.read().strip()
            if content.isdigit():
                count = int(content)
            else:
                print(f"⚠️ Некорректное содержимое файла: '{content}'. Сбрасываем на 0.")
    except Exception as e:
        print(f"⚠️ Ошибка при чтении файла: {e}. Сбрасываем на 0.")

    count += 1

    # Пишем новое значение
    try:
        with open(COUNTER_FILE, "w") as f:
            f.write(str(count))
    except Exception as e:
        print(f"⚠️ Ошибка при записи файла: {e}")

    print(f"Сканирований: {count}")
    return redirect("https://xn--80aicbopm7a.xn--d1aqf.xn--p1ai/", code=302)

@app.route('/reset')
def reset_counter():
    try:
        with open(COUNTER_FILE, "w") as f:
            f.write("0")
        return "<h2>✅ Счётчик успешно сброшен на 0!</h2><p><a href='/'>← Вернуться</a></p>"
    except Exception as e:
        return f"<h2>❌ Ошибка при сбросе: {e}</h2><p><a href='/'>← Вернуться</a></p>"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
