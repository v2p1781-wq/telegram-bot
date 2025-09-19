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

def get_mono_balance():
    if not MONO_TOKEN:
        return "Помилка: MONO_TOKEN не заданий у змінних середовища."

    headers = {"X-Token": MONO_TOKEN}   # <-- тут словник, все ок
    try:
        r = requests.get(MONO_API, headers=headers, timeout=10)
        r.raise_for_status()
    except Exception as e:
        return f"Помилка при запиті: {e}"

    data = r.json()
    balances = []
    for acc in data.get("accounts", []):
        balance = acc["balance"] / 100  # копійки → грн
        currency = acc["currencyCode"]
        iban = acc.get("iban", "—")
        balances.append(f"IBAN: {iban}, Баланс: {balance:.2f} {currency}")
        if acc["type"] == "yellow":
            balanda = acc["balance"] / 100
    return balanda

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
                now = int(time.time())

                # Відповідь тільки на /kolko і тільки якщо повідомлення свіже (≤40 хв)
                if text.strip().lower() == "/kolko" and (now - msg_time <= 40 * 60):
                    balance_info = get_mono_balance()
                    send_message(chat_id, balance_info)
                delete_message(chat_id, message_id)

if __name__ == "__main__":
    main()







