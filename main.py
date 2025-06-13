# === SETUP ===
import json
import requests
import websocket
import threading
import time

# === TELEGRAM ===
TOKEN = "7929662766:AAEnL_VsaMi_iBCqRd4CZGnFBe3HST-J1jI"
CHAT_ID = "1392975690"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram error:", e)

# === LIST PAIR & FILTER MINIMAL QTY ===
watchlist = ["BTCUSDT", "XRPUSDT", "DOGEUSDT"]
MIN_QTY = {
    "BTCUSDT": 0.3,
    "ETHUSDT": 3,
    "XRPUSDT": 100,
    "DOGEUSDT": 300,
    "SOLUSDT": 20,
    "1000SATSUSDT": 50000
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
                send_telegram_message(text)
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

# === RUNNING FUNCTION ===
def run_websocket():
    ws = websocket.WebSocketApp(ws_url,
                                 on_open=on_open,
                                 on_close=on_close,
                                 on_error=on_error,
                                 on_message=on_message)
    ws.run_forever()

# === JALANKAN DI THREAD TERPISAH ===
thread = threading.Thread(target=run_websocket)
thread.start()
