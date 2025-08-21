# Binance Liquidation Monitor dengan Gemini AI & Docker

Sistem monitoring liquidasi real-time dari Binance Futures yang terintegrasi dengan n8n, Gemini AI, dan Telegram notifications, semuanya berjalan dalam Docker containers.

## 🚀 Fitur Utama

- **Real-time Liquidation Monitoring**: WebSocket connection ke Binance Futures untuk XRP, DOGE, dan PEPE
- **Gemini AI Analysis**: Analisis cerdas menggunakan Google Gemini 1.5 Flash untuk rekomendasi trading
- **N8N Workflow Automation**: Workflow otomatis dengan visual interface
- **Telegram Notifications**: Alert real-time ke multiple chat dengan format yang informatif
- **Docker Deployment**: Containerized deployment untuk portabilitas dan skalabilitas
- **Health Monitoring**: Built-in health checks dan status monitoring
- **Auto-Reconnection**: Automatic reconnection untuk WebSocket connections
- **Fallback Processing**: Backup processing jika n8n webhook gagal

## 🏗️ Arsitektur Sistem

### Container Architecture
```
┌─────────────────┐    ┌─────────────────┐
│   N8N Container │    │ Monitor Container│
│                 │    │                 │
│ - Workflow UI   │◄──►│ - WebSocket     │
│ - Webhook API   │    │ - Gemini AI     │
│ - Gemini AI     │    │ - Telegram      │
│ - Telegram Bot  │    │ - Health Check  │
└─────────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────────────────────────────┐
│           Shared Network                │
│        (n8n-network)                    │
└─────────────────────────────────────────┘
```

### Data Flow
1. **Binance WebSocket** → Liquidation data
2. **Monitor Container** → Process & send to N8N webhook
3. **N8N Workflow** → Gemini AI analysis + Telegram formatting
4. **Telegram API** → Send notifications to users
5. **Fallback Path** → Direct processing jika N8N gagal

## 📋 Komponen Sistem

### 1. N8N Container (`n8nio/n8n:latest`)
- **Port**: 5678 (Web UI & Webhook API)
- **Environment**: Gemini API key, Telegram bot token
- **Volumes**: Persistent data storage
- **Features**: 
  - Visual workflow editor
  - Webhook triggers
  - Gemini AI integration
  - Telegram notifications

### 2. Liquidation Monitor Container (Custom Build)
- **Port**: 8080 (Health checks)
- **Base Image**: `python:3.11-slim`
- **Features**:
  - WebSocket monitoring
  - Gemini AI analysis (fallback)
  - Telegram notifications (fallback)
  - Health check endpoints
  - Auto-reconnection logic

### 3. Shared Resources
- **Network**: `n8n-network` (bridge)
- **Volumes**: 
  - `n8n_data`: N8N persistent data
  - `./logs`: Application logs
  - `./data`: Liquidation data backup

## 🛠️ Setup dan Instalasi

### Prerequisites
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Quick Start
```bash
# 1. Clone atau download semua files
# 2. Jalankan startup script
./docker-start.sh
```

### Manual Setup
```bash
# 1. Create directories
mkdir -p logs data workflows credentials custom-nodes

# 2. Copy environment file
cp .env.example .env
# Edit .env dengan API keys yang sesuai

# 3. Build dan start containers
docker-compose up -d

# 4. Check status
docker-compose ps
docker-compose logs -f
```

## 🔧 Konfigurasi

### Environment Variables (.env)
```bash
# Gemini AI
GEMINI_API_KEY=your_gemini_api_key_here

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID_1=your_chat_id_1
TELEGRAM_CHAT_ID_2=your_chat_id_2

# Binance Symbols
BINANCE_SYMBOLS=XRPUSDT,DOGEUSDT,PEPEUSDT

# N8N Configuration
N8N_HOST=0.0.0.0
N8N_PORT=5678
N8N_ENCRYPTION_KEY=your_encryption_key_here
```

### Docker Compose Services

#### N8N Service
```yaml
n8n:
  image: n8nio/n8n:latest
  ports:
    - "5678:5678"
  environment:
    - GEMINI_API_KEY=${GEMINI_API_KEY}
    - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
  volumes:
    - n8n_data:/home/node/.n8n
```

#### Monitor Service
```yaml
liquidation-monitor:
  build:
    context: .
    dockerfile: Dockerfile.monitor
  ports:
    - "8080:8080"
  environment:
    - N8N_WEBHOOK_URL=http://n8n:5678/webhook/liquidation-webhook
    - GEMINI_API_KEY=${GEMINI_API_KEY}
```

## 🚀 Cara Menjalankan

### Opsi 1: Quick Start (Recommended)
```bash
# Jalankan startup script
./docker-start.sh

# Script akan:
# - Check Docker installation
# - Create necessary directories
# - Copy .env file
# - Build dan start containers
# - Show status dan logs
```

### Opsi 2: Manual Docker Compose
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart
```

### Opsi 3: Development Mode
```bash
# Start dengan rebuild
docker-compose up --build

# Start specific service
docker-compose up n8n
docker-compose up liquidation-monitor
```

## 📊 Monitoring dan Management

### Web Interfaces
- **N8N Web UI**: http://localhost:5678
- **Health Check**: http://localhost:8080/health
- **Status Check**: http://localhost:8080/status
- **Test Notification**: http://localhost:8080/test-notification

### Docker Commands
```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f [service_name]

# Execute commands in container
docker-compose exec n8n bash
docker-compose exec liquidation-monitor bash

# View resource usage
docker stats

# Clean up
docker-compose down -v  # Remove volumes
docker system prune     # Clean unused resources
```

### Health Monitoring
```bash
# Check health status
curl http://localhost:8080/health

# Check detailed status
curl http://localhost:8080/status

# Test Telegram notifications
curl http://localhost:8080/test-notification
```

## 🔍 N8N Workflow Configuration

### Workflow Import
1. Access N8N Web UI: http://localhost:5678
2. Go to Workflows → Import
3. Upload `n8n_workflow_gemini_docker.json`
4. Activate the workflow

### Workflow Nodes
1. **Webhook Trigger**: Receives liquidation data
2. **Symbol Filter**: Filters XRP, DOGE, PEPE
3. **Get Market Data**: Fetches current market data
4. **Get Price History**: Fetches price history
5. **Gemini AI Analysis**: AI analysis dengan Gemini
6. **Format Message**: Format untuk Telegram
7. **Send Telegram**: Send ke multiple chats
8. **Webhook Response**: Response confirmation

### Environment Variables dalam N8N
- `GEMINI_API_KEY`: Untuk Gemini AI analysis
- `TELEGRAM_BOT_TOKEN`: Untuk Telegram API
- `TELEGRAM_CHAT_ID_1`: Chat ID pertama
- `TELEGRAM_CHAT_ID_2`: Chat ID kedua

## 📱 Format Alert Telegram

### Sample Alert Message
```
🚨 LIQUIDATION ALERT 🚨

🔴 XRPUSDT
💥 SELL Liquidation

📊 Liquidation Details:
• Price: $0.5234
• Quantity: 15,000
• Time: 14:30:25 UTC

🤖 Gemini AI Analysis:
🟢 📈 Recommendation: BUY
🎯 Confidence: 78%
🟡 Risk Level: MEDIUM
🐂 Market Sentiment: bullish

📈 Market Data:
• Current Price: $0.5412
• 24h Change: -2.80%
• Trend: 📉 Bearish
• Volatility: 4.20%
• RSI: 32.5

💡 AI Reasoning:
Large long liquidation below 24h average suggests oversold condition with potential bounce opportunity

🔑 Key Factors:
• Liquidation price 3.2% below current market price
• Volume spike indicates increased selling pressure
• Technical indicators show oversold conditions

📋 Strategy:
Consider DCA entry with 2-3% stop loss

🔬 Technical Data:
• SMA 12h: $0.5456
• Volume Ratio: 2.3x
• Impact: medium

⚡ Powered by Gemini AI
⚠️ This is automated analysis for informational purposes only. Always do your own research before trading.
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Container Won't Start
```bash
# Check logs
docker-compose logs [service_name]

# Check port conflicts
netstat -tlnp | grep :5678
netstat -tlnp | grep :8080

# Restart services
docker-compose restart
```

#### 2. N8N Workflow Issues
```bash
# Check N8N logs
docker-compose logs n8n

# Restart N8N
docker-compose restart n8n

# Check environment variables
docker-compose exec n8n env | grep GEMINI
```

#### 3. WebSocket Connection Issues
```bash
# Check monitor logs
docker-compose logs liquidation-monitor

# Test connectivity
docker-compose exec liquidation-monitor ping fstream.binance.com

# Restart monitor
docker-compose restart liquidation-monitor
```

#### 4. Telegram Notifications Gagal
```bash
# Test bot token
curl "https://api.telegram.org/bot<TOKEN>/getMe"

# Test notification endpoint
curl http://localhost:8080/test-notification

# Check chat IDs
curl "https://api.telegram.org/bot<TOKEN>/getUpdates"
```

### Performance Tuning

#### Resource Limits
```yaml
services:
  n8n:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
```

#### Log Rotation
```yaml
services:
  n8n:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## 📊 Monitoring dan Metrics

### Health Checks
```bash
# Container health
docker-compose ps

# Application health
curl http://localhost:8080/health

# N8N health
curl http://localhost:5678/healthz
```

### Metrics Collection
```bash
# Container stats
docker stats

# Application metrics
curl http://localhost:8080/status

# Log analysis
docker-compose logs --since 1h | grep "ERROR"
```

### Alerting Setup
```bash
# Setup monitoring alerts
# - Container down alerts
# - High memory usage
# - WebSocket disconnections
# - API failures
```

## 🔐 Security Considerations

### API Keys Management
- Store API keys dalam environment variables
- Jangan commit API keys ke repository
- Rotate API keys secara berkala
- Monitor API usage dan limits

### Network Security
```yaml
networks:
  n8n-network:
    driver: bridge
    internal: false  # Set true untuk isolasi
```

### Container Security
```dockerfile
# Run as non-root user
USER 1000:1000

# Minimal base image
FROM python:3.11-slim

# Security updates
RUN apt-get update && apt-get upgrade -y
```

## 📈 Scaling dan Production

### Horizontal Scaling
```yaml
services:
  liquidation-monitor:
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
```

### Load Balancing
```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

### Database Upgrade
```yaml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: n8n
      POSTGRES_USER: n8n
      POSTGRES_PASSWORD: n8n
  
  n8n:
    environment:
      DB_TYPE: postgresdb
      DB_POSTGRESDB_HOST: postgres
```

## 🚀 Deployment Options

### Local Development
```bash
# Development dengan hot reload
docker-compose -f docker-compose.dev.yml up
```

### Production Deployment
```bash
# Production dengan optimizations
docker-compose -f docker-compose.prod.yml up -d
```

### Cloud Deployment
```bash
# AWS ECS, Google Cloud Run, Azure Container Instances
# Kubernetes deployment dengan Helm charts
# Docker Swarm untuk multi-node deployment
```

## 📝 Maintenance

### Regular Tasks
```bash
# Update containers
docker-compose pull
docker-compose up -d

# Backup data
docker run --rm -v n8n_data:/backup alpine tar czf - /backup > n8n_backup.tar.gz

# Clean logs
docker-compose exec n8n find /home/node/.n8n/logs -name "*.log" -mtime +7 -delete

# Monitor disk usage
docker system df
```

### Backup Strategy
```bash
# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker run --rm -v n8n_data:/backup alpine tar czf - /backup > "backups/n8n_${DATE}.tar.gz"
find backups/ -name "n8n_*.tar.gz" -mtime +30 -delete
```

## 🎯 Performance Metrics

### Expected Performance
- **Latency**: < 2 detik dari liquidation ke notification
- **Throughput**: 100+ liquidations per minute
- **Uptime**: 99.9% dengan auto-reconnection
- **Memory Usage**: < 512MB per container
- **CPU Usage**: < 50% under normal load

### Optimization Tips
- Use connection pooling untuk HTTP requests
- Implement caching untuk market data
- Optimize Gemini AI prompt length
- Use async processing untuk notifications
- Monitor dan tune garbage collection

## 📞 Support dan Troubleshooting

### Debug Mode
```bash
# Enable debug logging
docker-compose -f docker-compose.debug.yml up

# Interactive debugging
docker-compose exec liquidation-monitor python -m pdb integrated_liquidation_system_docker.py
```

### Common Solutions
1. **Port conflicts**: Change ports dalam docker-compose.yml
2. **Memory issues**: Increase container limits
3. **API rate limits**: Implement backoff strategies
4. **Network issues**: Check firewall dan DNS
5. **Permission issues**: Check file permissions dan user IDs

### Getting Help
- Check logs: `docker-compose logs -f`
- Verify configuration: `docker-compose config`
- Test components individually
- Monitor resource usage
- Check API status pages

## 🔄 Updates dan Upgrades

### Container Updates
```bash
# Update to latest versions
docker-compose pull
docker-compose up -d

# Rollback if needed
docker-compose down
docker-compose up -d --force-recreate
```

### Configuration Updates
```bash
# Update environment variables
vim .env

# Restart affected services
docker-compose restart n8n liquidation-monitor
```

### Feature Additions
- Add new cryptocurrency pairs
- Implement additional AI models
- Add more notification channels
- Enhance monitoring capabilities
- Implement advanced trading strategies

