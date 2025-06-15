# === SETUP ===
import json
import requests
import websocket
import threading
import time
import pandas as pd

# === TELEGRAM ===
TOKEN = "7929662766:AAEnL_VsaMi_iBCqRd4CZGnFBe3HST-J1jI"
CHAT_IDS = [
    "1392975690",   # aku kamu
    "5841838340",   # akun teman
]

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    for chat_id in CHAT_IDS:
        payload = {"chat_id": chat_id, "text": message}
        try:
            requests.post(url, data=payload)
        except Exception as e:
            print(f"Telegram error to {chat_id}:", e)

# === PAIR & FILTER ===
watchlist = [
    "XRPUSDT", "DOGEUSDT", "PEPEUSDT",
    "SHIBUSDT", "1000PEPEUSDT", "WIFUSDT",
    "ARBUSDT", "LINKUSDT", "RNDRUSDT"
]

MIN_QTY = {
    "XRPUSDT": 100,
    "DOGEUSDT": 300,
    "PEPEUSDT": 5_000_000,
    "SHIBUSDT": 1_000_000,
    "1000PEPEUSDT": 5_000,
    "WIFUSDT": 100,
    "ARBUSDT": 10,
    "LINKUSDT": 2,
    "RNDRUSDT": 5
}

# === INDICATOR FUNCTION ===
def fetch_price_data(symbol, interval="1m", limit=30):
    try:
        url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={interval}&limit={limit}"
        data = requests.get(url, timeout=5).json()
        df = pd.DataFrame(data, columns=[
            'time', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base', 'taker_buy_quote', 'ignore'
        ])
        df['open'] = df['open'].astype(float)
        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(float)
        return df
    except Exception as e:
        print("Fetch price error:", e)
        return None

def is_bullish(candle):
    return candle['close'] > candle['open']

def volume_spike(volume, avg_volume):
    return volume > avg_volume * 1.2

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
                    return
                side = order.get("S", "")  # BUY or SELL
                price = float(order.get("p", 0))
                direction = "🔴 Long Liquidated" if side == "SELL" else "🟢 Short Liquidated"
                
                # Build base message
                text = (
                    f"💥 Liquidation Alert\n"
                    f"Symbol: {symbol}\n"
                    f"{direction}\n"
                    f"Side: {side}\n"
                    f"Qty: {qty:,.2f}\n"
                    f"Price: {price:,.4f}"
                )

                # Tambahkan logika sinyal tambahan
                df = fetch_price_data(symbol)
                if df is not None and len(df) >= 20:
                    latest = {
                        'open': df['open'].iloc[-2],
                        'close': df['close'].iloc[-2]
                    }
                    volume_now = df['volume'].iloc[-2]
                    avg_volume = df['volume'].iloc[:-2].mean()
                    price_now = df['close'].iloc[-1]
                    MA_20 = df['close'].iloc[-20:].mean()

                    signal = "WAIT 🟡"
                    if side == "BUY" and is_bullish(latest) and volume_spike(volume_now, avg_volume) and price_now > MA_20:
                        signal = "BUY ✅"
                    elif side == "SELL" and not is_bullish(latest) and not volume_spike(volume_now, avg_volume) and price_now < MA_20:
                        signal = "SELL ❌"

                    text += (
                        f"\n📊 Signal: {signal}"
                        f"\n📈 MA20: {MA_20:.5f}"
                        f"\n📊 Volume: {volume_now:,.0f}"
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
