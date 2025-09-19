import requests
import os
import time

TOKEN = os.getenv("BOT_TOKEN")
API = f"https://api.telegram.org/bot{TOKEN}"

# Твій токен Monobank
MONO_TOKEN = os.getenv("MONO_TOKEN")
MONO_API = "https://api.monobank.ua/personal/client-info"

def get_updates(offset=None, timeout=10):
    params = {"timeout": timeout}
    if offset:
        params["offset"] = offset
    r = requests.get(API + "/getUpdates", params=params)
    return r.json()

def send_message(chat_id, text):
    requests.post(API + "/sendMessage", data={"chat_id": chat_id, "text": text})

def delete_message(chat_id, message_id):
    """Видалення повідомлення користувача"""
    requests.post(API + "/deleteMessage", data={"chat_id": chat_id, "message_id": message_id})

def get_mono_balance():
    if not MONO_TOKEN:
        return "Помилка: MONO_TOKEN не заданий у змінних середовища."

    headers = {"X-Token": MONO_TOKEN}
    try:
        r = requests.get(MONO_API, headers=headers, timeout=10)
        r.raise_for_status()
    except Exception as e:
        return f"Помилка при запиті: {e}"

    data = r.json()
    balances = []
    balanda = None
    for acc in data.get("accounts", []):
        balance = acc["balance"] / 100
        currency = acc["currencyCode"]
        iban = acc.get("iban", "—")
        balances.append(f"IBAN: {iban}, Баланс: {balance:.2f} {currency}")
        if acc["type"] == "yellow":
            balanda = acc["balance"] / 100
    return balanda if balanda is not None else "\n".join(balances)

def main():
    offset = None
    res = get_updates(offset)
    if res.get("ok"):
        for upd in res["result"]:
            offset = upd["update_id"] + 1
            if "message" in upd:
                chat_id = upd["message"]["chat"]["id"]
                text = upd["message"].get("text", "")
                msg_time = upd["message"].get("date")
                message_id = upd["message"]["message_id"]
                now = int(time.time())

                # Відповідь тільки на /kolko і якщо повідомлення свіже
                if text.strip().lower() == "/kolko" and (now - msg_time <= 40 * 60):
                    balance_info = get_mono_balance()
                    send_message(chat_id, balance_info)

                # Видаляємо повідомлення користувача після обробки
                delete_message(chat_id, message_id)

if __name__ == "__main__":
    main()


