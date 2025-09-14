import requests
import os

MONO = os.getenv("MONO_TOKEN")
MONO_API = "https://api.monobank.ua/personal/client-info"

def get_mono_balance():
    headers = {{MONO}}
    r = requests.get(MONO_API, headers=headers)
    if r.status_code == 200:
        data = r.json()
        balances = []
        for acc in data["accounts"]:
            balance = acc["balance"] / 100  # копійки → грн
            currency = acc["currencyCode"]
            iban = acc.get("iban", "—")
            balances.append(f"IBAN: {iban}, Баланс: {balance:.2f} {currency}")
        return "\n".join(balances)
    else:
        return f"Помилка: {r.status_code}, {r.text}"

if __name__ == "__main__":
    print(get_mono_balance())
