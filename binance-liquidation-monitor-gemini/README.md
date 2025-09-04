# Binance Liquidation Monitor (Gemini Edition)

Monorepo yang merangkum semua dokumentasi dan skeleton project untuk **sistem monitoring likuidasi Binance Futures**
dengan **analisis AI (Gemini)**, **n8n workflow**, **Telegram notifications**, serta **rencana web dashboard**.

> Koin yang difokuskan: **XRP, DOGE, PEPE** (`xrpusdt@forceOrder`, `dogeusdt@forceOrder`, `pepeusdt@forceOrder`).

## 📚 Isi Repo

- `docs/` — dokumentasi terkurasi (dirapikan & dinomori)
  - 01_system_xrp_gemini.md — fokus XRP + threshold + arsitektur
  - 02_dashboard_realtime_price.md — integrasi harga realtime (CoinGecko) untuk dashboard
  - 03_docker_deployment.md — arsitektur & setup Docker (n8n + monitor)
  - 04_dashboard_website.md — dokumentasi website dashboard (React + Flask)
  - 05_system_ai_analysis.md — sistem monitoring dgn AI analysis & Telegram
  - 06_binance_liquidation_api_info.md — info stream `@forceOrder`
- `workflows/` — placeholder workflow **n8n** (silakan ganti dengan file asli Anda)
- `docker/` — `docker-compose.yml` + `Dockerfile.monitor` + contoh `.env.example`
- `scripts/` — **monitor_placeholder.py** agar stack Docker bisa *run/health-check* sambil menunggu kode monitor final, serta contoh bot **ma_rsi_trading_bot.py** yang menggunakan indikator MA dan RSI untuk trading otomatis
- `backend/`, `frontend/` — placeholder README untuk struktur ke depan

## 🚀 Quick Start (Docker, untuk demonstrasi layanan & health endpoint)
> Ini masih **skeleton** (belum konek ke Binance/Gemini). Tujuannya biar **stack hidup**, endpoint health/status ada,
> dan gampang nanti diganti dengan implementasi final Anda.

1. Siapkan environment:
    ```bash
    cd docker
    cp .env.example .env
    # edit .env sesuai kebutuhan (GEMINI_API_KEY, TELEGRAM_* dll)
    ```

2. Jalankan:
    ```bash
    docker compose up -d --build
    ```

3. Cek:
    - N8N UI: http://localhost:5678
    - Health monitor (placeholder): http://localhost:8080/health
    - Status monitor (placeholder): http://localhost:8080/status
    - Test notification (placeholder): http://localhost:8080/test-notification

## 🔄 Ganti ke Monitor Sungguhan
- Ganti `scripts/monitor_placeholder.py` dengan implementasi **monitor asli** (WebSocket Binance + Gemini + Telegram + n8n webhook) sesuai dokumentasi.
- Jika Anda sudah punya file seperti `integrated_liquidation_system_docker.py`, sesuaikan `Dockerfile.monitor` dan `docker-compose.yml` (command & dependencies).

## 🧩 n8n Workflow
- Import workflow Anda ke n8n (menu **Workflows → Import**).
- Contoh nama file: `n8n_workflow_gemini_docker.json`.
- Placeholder ada di `workflows/n8n_workflow_placeholder.json` untuk menunjukkan struktur.

## ⚙️ Environment Variables (contoh)
Lihat `docker/.env.example` — gunakan sesuai kebutuhan:
- `GEMINI_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID_*`
- `BINANCE_SYMBOLS=XRPUSDT,DOGEUSDT,PEPEUSDT`
- `N8N_*` configs (host, port, encryption key)

## 📦 Struktur Folder
```
binance-liquidation-monitor-gemini/
├─ docs/
├─ workflows/
├─ docker/
├─ scripts/
├─ backend/
├─ frontend/
└─ README.md
```

## 📄 Lisensi
MIT — silakan gunakan & modifikasi.
