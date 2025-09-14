import requests
import os
import time

TOKEN = os.getenv("BOT_TOKEN")
API = f"https://api.telegram.org/bot{TOKEN}"

def get_updates(offset=None, timeout=10):
    params = {"timeout": timeout}
    if offset:
        params["offset"] = offset
    r = requests.get(API + "/getUpdates", params=params)
    return r.json()

def send_message(chat_id, text):
    requests.post(API + "/sendMessage", data={"chat_id": chat_id, "text": text})


def main():
    offset = None
    res = get_updates(offset)
    if res.get("ok"):
        for upd in res["result"]:
            offset = upd["update_id"] + 1
            if "message" in upd:
                chat_id = upd["message"]["chat"]["id"]
                text = upd["message"].get("text", "")
                msg_time = upd["message"].get("date")  # UNIX timestamp
                now = int(time.time())

                # Перевіряємо чи повідомлення не старше 15 хвилин
                if now - msg_time <= 15 * 60:
                    send_message(chat_id, "Echo: " + text)

if __name__ == "__main__":
    main()



