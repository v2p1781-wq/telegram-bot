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
    return "\n".join(balances)
