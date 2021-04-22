from flask import Flask, request, abort
import time
from datetime import datetime


app = Flask(__name__)


db = [
    {
        "name": "",
        "text": "",
        "time": time.time()
    },

]

@app.route("/")
def hello():
    return "meh"



@app.route("/status")
def status():
    dt = datetime.now()
    # Количество сообщений
    msg = 0
    # Список для отображения всех пользователей в /status
    users = []
    users_total = 0

    for i in db:
        if i["name"] not in users:
            users.append(i["name"])
            users_total += 1

    for j in db:
        if j["text"] != "":
            msg += 1

    return {
        "status": True,
        "name": "My test messenger",
        "Current time": dt.strftime("%Y/%m/%d %H:%M"),
        "Total users": users_total,
        "Total messages": msg,
        # Выведем всех юзеров потому что почему бы и нет
        "Users": ", ".join(users)
    }


@app.route("/time_page")
def time_page():
    return {
        "status": True,
        "name": "My Messenger",
        "time": time.asctime(),
    }


@app.route("/send", methods=["POST"])
def send_message():
    data = request.json

    if not isinstance(data, dict):
        return abort(400)
    if "name" not in data or "text" not in data:
        return abort(400)

    name = data["name"]
    text = data["text"]

    if not isinstance(name, str) or not isinstance(text, str):
        return abort(400)
    if name == "" or text == "":
        return abort(400)

    db.append({
        "name": name,
        "text": text,
        "time": time.time()
    })

    if text == "/help":
        db.append({
            "name": "Bot",
            "text": """Вы воспользовались командой /help. 
            Доступны следующие функции: 
            /time - выведет на экран время
            /msg - выведет количество сообщений в чате
            /users - выведет количество активных пользователей
            """,
            "time": time.time()
        })

    if text == "/time":
        db.append({
            "name": "Bot",
            "text": f"Сейчас на часах: {datetime.now().strftime('%Y/%m/%d %H:%M')}",
            "time": time.time()
        })
    if text == "/msg":
        # Вызываем функцию статус для получения данных о количестве сообщений
        data = status()
        db.append({
            "name": "Bot",
            "text": f'Всего сообщений в чате: {data["Total messages"]}',
            "time": time.time()
        })
    if text == "/users":
        # Вызываем функцию статус для получения данных о количестве пользователей
        data = status()
        db.append({
            "name": "Bot",
            "text": f'Всего пользователей в чате: {data["Total users"]}',
            "time": time.time()
        })


    return {"ok": True}


@app.route("/messages")
def get_messages():
    try:
        after = float(request.args["after"])
    except:
        return abort(400)

    messages = []
    for message in db:
        if message["time"] > after:
            messages.append(message)
    return {"messages": messages[:50]}


app.run(debug=True)