from flask import Flask, jsonify, request
import os, time, random

app = Flask(__name__)

START = time.time()

@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "liquidation-monitor-placeholder"}), 200

@app.get("/status")
def status():
    uptime = time.time() - START
    return jsonify({
        "status": "running",
        "uptime_sec": int(uptime),
        "processed_today": random.randint(0, 10),
        "ai_enabled": True,
        "symbols": os.getenv("BINANCE_SYMBOLS", "XRPUSDT,DOGEUSDT,PEPEUSDT").split(","),
        "note": "This is a placeholder. Replace with real Binance WebSocket + Gemini + Telegram + n8n webhook implementation."
    }), 200

@app.get("/test-notification")
def test_notification():
    # Here you could call Telegram/n8n webhook for a smoke test in the real implementation.
    return jsonify({"ok": True, "message": "Test notification placeholder (implement real call here)."}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
