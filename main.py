# === SETUP ===
import json
import requests
import websocket
import threading
import time

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
            requests.post(url, data=payload)
        except Exception as e:
            print(f"Telegram error to {chat_id}:", e)

# === N8N WEBHOOK ===
def send_to_n8n(symbol, side, qty, price):
    webhook_url = "https://crop-recognized-aspect-turkey.trycloudflare.com/webhook-test/liquidation-alert"
    payload = {
        "symbol": symbol,
        "side": side,
        "qty": qty,
        "price": price
    }
    try:
        response = requests.post(webhook_url, json=payload)
        print(f"✅ Dikirim ke N8N: {response.status_code}, {response.text}")
    except Exception as e:
        print("❌ Gagal kirim ke N8N:", e)

# === LIST PAIR & FILTER MINIMAL QTY ===
watchlist = [
    "XRPUSDT", "DOGEUSDT", "PEPEUSDT",
    "SHIBUSDT", "1000PEPEUSDT", "WIFUSDT",
    "ARBUSDT", "LINKUSDT", "RNDRUSDT"
]

MIN_QTY = {
    "XRPUSDT": 100,
    "DOGEUSDT": 300,
    "PEPEUSDT": 5000000,
    "SHIBUSDT": 1000000,
    "1000PEPEUSDT": 5000,
    "WIFUSDT": 100,
    "ARBUSDT": 10,
    "LINKUSDT": 2,
    "RNDRUSDT": 5
}

# === COMBINE STREAM URL ===
stream_names = [f"{symbol.lower()}@forceOrder" for symbol in watchlist]
ws_url = f"wss://fstream.binance.com/stream?streams={'/'.join(stream_names)}"

# === CALLBACK WEBSOCKET ===
def on_message(ws, message):
    try:
        msg = json.loads(message)
        data = msg.get("data", {})
        if "o" in data:
            order = data["o"]
            symbol = order.get("s", "")
            if symbol in watchlist:
                qty = float(order.get("q", 0))
                if qty < MIN_QTY[symbol]:
                    return  # skip kecil
                side = order.get("S", "")  # BUY or SELL
                price = float(order.get("p", 0))
                direction = "🔴 Long Liquidated" if side == "SELL" else "🟢 Short Liquidated"
                text = (
                    f"💥 Liquidation Alert\n"
                    f"Symbol: {symbol}\n"
                    f"{direction}\n"
                    f"Side: {side}\n"
                    f"Qty: {qty:,.2f}\n"
                    f"Price: {price:,.4f}"
                )
                print(text)

                # Kirim ke n8n, bukan Telegram langsung
                send_to_n8n(symbol, side, qty, price)

    except Exception as e:
        print("Parsing error:", e)

def on_open(ws):
    print("✅ WebSocket connected!")

def on_close(ws, close_status_code, close_msg):
    print("❌ WebSocket disconnected. Reconnecting in 5s...")
    time.sleep(5)
    run_websocket()

def on_error(ws, error):
    print("WebSocket error:", error)

# === JALANKAN ===
def run_websocket():
    ws = websocket.WebSocketApp(ws_url,
                                 on_open=on_open,
                                 on_close=on_close,
                                 on_error=on_error,
                                 on_message=on_message)
    ws.run_forever()

thread = threading.Thread(target=run_websocket)
thread.start()
