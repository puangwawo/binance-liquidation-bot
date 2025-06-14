import requests

# === TELEGRAM ===
TOKEN = "7929662766:AAEnL_VsaMi_iBCqRd4CZGnFBe3HST-J1jI"
CHAT_IDS = [
    "1392975690",   # aku kamu
    "5841838343",   # akun teman
]

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    for chat_id in CHAT_IDS:
        payload = {"chat_id": chat_id, "text": message}
        try:
            response = requests.post(url, data=payload)
            print(f"[{chat_id}] Status: {response.status_code}")
            print(response.text)
        except Exception as e:
            print(f"Telegram error to {chat_id}:", e)
