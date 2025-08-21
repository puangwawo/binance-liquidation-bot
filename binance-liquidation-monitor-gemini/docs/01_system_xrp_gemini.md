# Dokumentasi Sistem Monitoring Liquidasi XRP dengan Gemini AI

## Pendahuluan

Dokumen ini menjelaskan sistem monitoring liquidasi XRP yang disederhanakan, dirancang untuk memberikan sinyal trading yang lebih actionable berdasarkan ambang batas likuidasi spesifik dan analisis AI menggunakan Gemini 1.5 Flash. Sistem ini berfokus secara eksklusif pada pasangan trading XRPUSDT di Binance Futures, mengintegrasikan filter nilai likuidasi per peristiwa, ambang kumulatif dalam periode waktu tertentu, dan deteksi 'spike' likuidasi dua arah untuk mengidentifikasi tekanan pasar yang signifikan.

## Arsitektur Sistem

Sistem ini terdiri dari beberapa komponen utama yang bekerja secara sinergis untuk memantau, menganalisis, dan memberikan notifikasi likuidasi XRP:

1.  **WebSocket Listener Binance Futures**: Komponen ini secara real-time mendengarkan aliran data `forceOrder` dari Binance Futures untuk pasangan XRPUSDT. Ini memastikan bahwa setiap peristiwa likuidasi terdeteksi segera setelah terjadi.
2.  **Logic Filtering Likuidasi**: Data likuidasi yang masuk akan melewati serangkaian filter yang telah ditentukan untuk memastikan hanya peristiwa yang relevan dan signifikan yang diproses lebih lanjut. Filter ini mencakup nilai likuidasi per peristiwa dan ambang kumulatif dalam jangka waktu 15 menit.
3.  **Gemini AI Analysis Engine**: Untuk setiap peristiwa likuidasi yang lolos filter, data akan dikirim ke Gemini 1.5 Flash API untuk analisis mendalam. AI akan memberikan rekomendasi trading (BUY/SELL/HOLD/WAIT), tingkat kepercayaan, penilaian risiko, faktor-faktor kunci, dan strategi yang disarankan.
4.  **Telegram Notifier**: Hasil analisis dan rekomendasi dari AI akan diformat menjadi pesan yang informatif dan dikirimkan secara otomatis ke grup atau chat Telegram yang telah dikonfigurasi. Notifikasi ini dirancang untuk memberikan informasi yang cepat dan mudah dicerna oleh trader.

## Parameter dan Thresholds

Sistem ini menggunakan parameter dan ambang batas spesifik untuk menyaring dan memprioritaskan sinyal likuidasi XRP. Parameter ini disesuaikan untuk mengidentifikasi 'whale' liquidations dan tekanan pasar yang sistematis, bukan hanya spike acak. Berikut adalah detail ambang batas yang digunakan:

| Parameter                       | Nilai Ambang Batas |
| :------------------------------ | :----------------- |
| Likuidasi per Peristiwa (XRPUSDT) | > $500.000         |
| Total Kumulatif 15 Menit        | > $1.500.000       |
| Spike Dua Arah (Long + Short)   | > $1.000.000       |

### Penjelasan Ambang Batas:

*   **Likuidasi per Peristiwa (> $500.000)**: Ambang batas ini memastikan bahwa hanya likuidasi individual yang berukuran besar yang diperhatikan. Likuidasi di bawah $500.000 dianggap sebagai 'noise' pasar yang kurang signifikan untuk strategi trading yang ditargetkan.
*   **Total Kumulatif 15 Menit (> $1.500.000)**: Ini adalah ambang batas kumulatif yang memantau total nilai likuidasi (baik long maupun short) dalam jendela waktu 15 menit. Jika total likuidasi melebihi $1.500.000 dalam periode ini, itu menunjukkan adanya tekanan pasar yang berkelanjutan atau aktivitas 'whale' yang signifikan. Ambang batas ini membedakan antara spike harga acak dan likuidasi sistematis yang dapat mengindikasikan pergeseran tren.
*   **Spike Dua Arah (Long + Short) (> $1.000.000)**: Ambang batas ini dirancang untuk mendeteksi pergerakan harga yang cepat dan signifikan yang disebabkan oleh likuidasi besar dari kedua sisi (long dan short) dalam waktu singkat. Total nilai likuidasi long dan short yang melebihi $1.000.000 dalam jendela 15 menit menunjukkan volatilitas ekstrem dan potensi peluang trading.

Ambang batas ini terintegrasi dengan kerangka waktu trading scalping 15–30 menit, menjadikan sinyal yang dihasilkan lebih 'actionable' dan relevan untuk keputusan trading cepat.

## Analisis AI dengan Gemini

Gemini 1.5 Flash digunakan untuk menganalisis setiap peristiwa likuidasi yang memenuhi kriteria ambang batas. AI menerima konteks data likuidasi, termasuk nilai per peristiwa, kumulatif 15 menit, dan nilai spike dua arah. Berdasarkan informasi ini, Gemini akan menghasilkan:

*   **Rekomendasi**: BUY, SELL, HOLD, atau WAIT.
*   **Tingkat Kepercayaan**: Persentase yang menunjukkan keyakinan AI terhadap rekomendasinya.
*   **Penilaian Risiko**: LOW, MEDIUM, atau HIGH, berdasarkan potensi volatilitas dan dampak pasar.
*   **Faktor Kunci**: Poin-poin penting yang mendasari analisis dan rekomendasi AI.
*   **Strategi**: Saran strategi trading spesifik untuk kerangka waktu 15-30 menit.
*   **Penalaran**: Penjelasan rinci mengapa AI memberikan rekomendasi tersebut.

AI dirancang untuk mengidentifikasi pola-pola yang menunjukkan tekanan pasar nyata, seperti likuidasi besar yang mendekati zona 'whale', di mana pergerakan harga yang signifikan lebih mungkin terjadi.

## Notifikasi Telegram

Setiap sinyal likuidasi yang diproses dan dianalisis oleh AI akan dikirimkan ke Telegram dalam format yang jelas dan ringkas. Notifikasi mencakup:

*   Detail likuidasi (simbol, sisi, kuantitas, harga, nilai).
*   Metrik 15 menit (kumulatif, total long, total short, total spike).
*   Rekomendasi AI (dengan tingkat kepercayaan dan risiko).
*   Faktor kunci dan penalaran AI.
*   Timestamp peristiwa.

Notifikasi juga akan menyertakan indikator 'HIGH CONFIDENCE SIGNAL' jika likuidasi kumulatif atau spike dua arah melebihi ambang batas yang ditentukan, menandakan peluang trading yang lebih kuat.

## Cara Menjalankan Sistem

Sistem ini dapat dijalankan sebagai skrip Python mandiri. Pastikan Anda memiliki Python 3, `websocket-client`, `requests`, dan `python-telegram-bot` terinstal. Untuk integrasi Gemini AI, pastikan Anda memiliki konektivitas ke Google Generative Language API dan API Key yang valid.

### Persyaratan:

*   Python 3.x
*   `pip install websocket-client requests python-telegram-bot`
*   Akses ke Google Gemini API dengan API Key yang valid.
*   Bot Token Telegram dan Chat ID yang valid.

### Konfigurasi:

Edit file `xrp_liquidation_monitor.py` dan perbarui variabel berikut:

```python
self.gemini_api_key = "YOUR_GEMINI_API_KEY"
self.bot_token = "YOUR_TELEGRAM_BOT_TOKEN"
self.chat_ids = ["YOUR_CHAT_ID_1", "YOUR_CHAT_ID_2"]
```

### Eksekusi:

```bash
python3 xrp_liquidation_monitor.py
```

Sistem akan mulai memantau likuidasi XRP dan mengirimkan notifikasi ke Telegram sesuai dengan ambang batas yang telah ditentukan.

## Kesimpulan

Sistem monitoring likuidasi XRP ini menyediakan alat yang kuat bagi trader untuk mengidentifikasi dan merespons peristiwa likuidasi yang signifikan di pasar Binance Futures. Dengan kombinasi filter ambang batas yang cermat dan analisis AI yang cerdas, sistem ini bertujuan untuk memberikan sinyal trading yang lebih akurat dan actionable, membantu trader membuat keputusan yang lebih tepat dalam lingkungan pasar yang volatil.

**Penulis:** Manus AI
**Tanggal:** 4 Agustus 2025


