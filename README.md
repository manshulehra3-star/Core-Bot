# 🚀 INFINITE CORE BOT

Production-Grade Hosting, Payment, Ticket & AI Automation Discord Bot.

---

## 🛠️ System Prerequisites (Linux VPS)
- Ubuntu 22.04 LTS or Debian 12
- Python 3.10+
- Ollama (Local AI Host)

---

## 🚀 Quick Installation Guide

### 1. System Dependencies & Virtual Environment
```bash
sudo apt update && sudo apt install -y python3 python3-venv python3-pip git curl
mkdir -p /opt/infinite-core-bot
cd /opt/infinite-core-bot
# Place bot source files into /opt/infinite-core-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
