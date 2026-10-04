🚀 INFINITE CORE BOT

Production-grade Discord bot for hosting automation, payments, tickets, server management and local AI.

""Python" (https://img.shields.io/badge/Python-3.10%2B-blue.svg)" (https://www.python.org/)
""Discord.py" (https://img.shields.io/badge/discord.py-2.3%2B-5865F2.svg)" (https://github.com/Rapptz/discord.py)
""License" (https://img.shields.io/badge/License-MIT-yellow.svg)" (LICENSE)

GitHub Repository: https://github.com/manshulehra3-star/Core-Bot

---

✨ Features

- Discord bot automation
- Hosting management
- Payment logging
- Ticket system
- Welcome/leave system
- Local AI using Ollama
- VPS/PANEL API integration
- SQLite database
- 24/7 systemd service
- Automatic restart after VPS reboot
- GitHub-based updates

---

🖥️ System Requirements

Supported OS

- Ubuntu 22.04 LTS
- Ubuntu 24.04 LTS
- Debian 12

Minimum

- 4 GB RAM
- 2 vCPU
- 10 GB free disk
- Python 3.10+

Recommended for Local AI

- 16–32 GB RAM
- 8+ vCPU
- SSD/NVMe storage

---

⚡ ONE-COMMAND INSTALLATION

On a fresh Ubuntu/Debian VPS, run:

sudo apt update && sudo apt upgrade -y && sudo apt install -y python3 python3-venv python3-pip git curl && git clone https://github.com/manshulehra3-star/Core-Bot.git && cd Core-Bot && python3 -m venv venv && source venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt && curl -fsSL https://ollama.com/install.sh | sh && sudo systemctl enable --now ollama && ollama pull qwen3.5:0.8b

After installation:

cd Core-Bot
source venv/bin/activate
cp .env.example .env
nano .env

Configure your ".env" file before starting the bot.

---

🛠️ Manual Installation

If you prefer installing step-by-step, follow the sections below.

Step 1 — Update System

sudo apt update
sudo apt upgrade -y

Step 2 — Install Dependencies

sudo apt install -y python3 python3-venv python3-pip git curl

Step 3 — Clone Repository

git clone https://github.com/manshulehra3-star/Core-Bot.git
cd Core-Bot

Step 4 — Create Python Virtual Environment

python3 -m venv venv
source venv/bin/activate

Step 5 — Upgrade pip

pip install --upgrade pip

Step 6 — Install Python Requirements

pip install -r requirements.txt

---

🤖 Install Ollama

Install Ollama:

curl -fsSL https://ollama.com/install.sh | sh

Enable and start Ollama:

sudo systemctl enable --now ollama

Verify Ollama:

ollama --version

Check service:

systemctl status ollama

---

🧠 Install Local AI Model

INFINITE CORE BOT uses Ollama for local AI.

The lightweight model used by default is:

qwen3.5:0.8b

Install it:

ollama pull qwen3.5:0.8b

Test it:

ollama run qwen3.5:0.8b

Type:

Hello

Exit with:

/bye

Check installed models:

ollama list

---

⚙️ Environment Configuration

Create the environment file:

cp .env.example .env

Edit it:

nano .env

Use the following structure:

# ==========================================
# DISCORD BOT
# ==========================================

DISCORD_TOKEN=your_bot_token_here
OWNER_ID=123456789012345678
GUILD_ID=123456789012345678


# ==========================================
# DATABASE
# ==========================================

DATABASE_PATH=./data/infinite_core.db


# ==========================================
# WELCOME / LEAVE
# ==========================================

WELCOME_CHANNEL_ID=123456789012345678
LEAVE_CHANNEL_ID=123456789012345678
WELCOME_DM_ENABLED=true


# ==========================================
# TICKETS
# ==========================================

TICKET_CATEGORY_ID=123456789012345678
TICKET_LOG_CHANNEL_ID=123456789012345678


# ==========================================
# PAYMENTS
# ==========================================

PAYMENT_LOG_CHANNEL_ID=123456789012345678
PAYMENT_OWNER_ID=123456789012345678


# ==========================================
# LOCAL AI / OLLAMA
# ==========================================

AI_ENABLED=true
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=qwen3.5:0.8b


# ==========================================
# SVM / VPS PANEL
# ==========================================

SVM_API_URL=https://vps.example.com/api
SVM_API_KEY=your_svm_api_key_here


# ==========================================
# MINECRAFT PANEL
# ==========================================

MC_PANEL_API_URL=https://mc.example.com/api
MC_PANEL_API_KEY=your_mc_panel_api_key_here

Replace all placeholder values with your real credentials and IDs.

Never publish your ".env" file or Discord bot token on GitHub.

---

🗄️ Database

The bot uses SQLite by default.

Database location:

./data/infinite_core.db

Create the data directory if required:

mkdir -p data

---

▶️ Run Bot Manually

Activate the virtual environment:

cd Core-Bot
source venv/bin/activate

Start the bot:

python3 bot.py

If the bot starts successfully, keep the terminal open while testing.

Stop it with:

CTRL+C

---

🔄 24/7 Production Setup

For production, use systemd instead of keeping the bot running inside SSH.

Create the service:

sudo nano /etc/systemd/system/infinite-core-bot.service

Add:

[Unit]
Description=INFINITE CORE Discord Bot
After=network-online.target ollama.service
Wants=network-online.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/Core-Bot
Environment="PATH=/root/Core-Bot/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin"
ExecStart=/root/Core-Bot/venv/bin/python /root/Core-Bot/bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target

«If your repository is installed somewhere other than "/root/Core-Bot", change the paths accordingly.»

Reload systemd:

sudo systemctl daemon-reload

Enable automatic startup:

sudo systemctl enable infinite-core-bot

Start the bot:

sudo systemctl start infinite-core-bot

Check status:

sudo systemctl status infinite-core-bot

---

📋 View Live Bot Logs

journalctl -u infinite-core-bot -f

View recent logs:

journalctl -u infinite-core-bot -n 100 --no-pager

View logs from the current boot:

journalctl -u infinite-core-bot -b --no-pager

---

🔧 Service Commands

Start

sudo systemctl start infinite-core-bot

Stop

sudo systemctl stop infinite-core-bot

Restart

sudo systemctl restart infinite-core-bot

Status

sudo systemctl status infinite-core-bot

Enable on Boot

sudo systemctl enable infinite-core-bot

Disable on Boot

sudo systemctl disable infinite-core-bot

---

🔄 Update Bot From GitHub

Go to the project:

cd /root/Core-Bot

Stop the bot:

sudo systemctl stop infinite-core-bot

Pull the latest version:

git pull origin main

Activate the virtual environment:

source venv/bin/activate

Update Python dependencies:

pip install -r requirements.txt --upgrade

Start the bot again:

sudo systemctl start infinite-core-bot

Check status:

sudo systemctl status infinite-core-bot

---

⚡ One-Command Update

Once the bot is already installed:

cd /root/Core-Bot && sudo systemctl stop infinite-core-bot && git pull origin main && source venv/bin/activate && pip install -r requirements.txt --upgrade && sudo systemctl start infinite-core-bot && sudo systemctl status infinite-core-bot --no-pager

---

🔁 Restart Everything

Restart Ollama and the bot:

sudo systemctl restart ollama && sudo systemctl restart infinite-core-bot

Check both:

systemctl status ollama --no-pager
sudo systemctl status infinite-core-bot --no-pager

---

🧪 Health Checks

Check Python

python3 --version

Check pip

pip3 --version

Check Git

git --version

Check Ollama

ollama --version

Check Ollama API

curl http://127.0.0.1:11434/api/tags

Check Installed AI Models

ollama list

Check Bot Service

sudo systemctl is-active infinite-core-bot

Expected:

active

---

❗ Troubleshooting

Bot Does Not Start

Check:

sudo systemctl status infinite-core-bot

Then:

journalctl -u infinite-core-bot -n 100 --no-pager

---

Check ".env"

cd /root/Core-Bot
cat .env

Do not share the output publicly because it contains secrets.

---

Discord Token Error

Verify:

DISCORD_TOKEN=your_real_bot_token

Make sure there are no unnecessary spaces or quotes.

---

Ollama Not Running

Run:

sudo systemctl restart ollama

Check:

systemctl status ollama

Test:

curl http://127.0.0.1:11434/api/tags

---

AI Model Missing

Check:

ollama list

Install:

ollama pull qwen3.5:0.8b

---

Python Dependency Error

cd /root/Core-Bot
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

Then:

sudo systemctl restart infinite-core-bot

---

Git Pull Error

Check repository status:

cd /root/Core-Bot
git status

If you have local changes, back them up before using destructive Git commands.

---

🔐 Security

Never upload these to GitHub:

.env
*.db
*.sqlite
*.sqlite3
__pycache__/
venv/

Recommended ".gitignore":

.env
*.db
*.sqlite
*.sqlite3
__pycache__/
*.pyc
venv/
.venv/

Never expose:

- Discord bot token
- API keys
- Panel API keys
- Database credentials
- Private SSH keys

---

📁 Recommended Project Structure

Core-Bot/
├── bot.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── infinite-core-bot.service
├── data/
│   └── infinite_core.db
└── venv/

---

🚀 Quick Start

Fresh VPS:

sudo apt update && sudo apt upgrade -y && sudo apt install -y python3 python3-venv python3-pip git curl && git clone https://github.com/manshulehra3-star/Core-Bot.git && cd Core-Bot && python3 -m venv venv && source venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt && curl -fsSL https://ollama.com/install.sh | sh && sudo systemctl enable --now ollama && ollama pull qwen3.5:0.8b

Configure:

cd /root/Core-Bot && cp .env.example .env && nano .env

Test:

cd /root/Core-Bot && source venv/bin/activate && python3 bot.py

Production:

sudo cp /root/Core-Bot/infinite-core-bot.service /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl enable --now infinite-core-bot

Logs:

journalctl -u infinite-core-bot -f

---

📜 License

This project is licensed under the MIT License.

See "LICENSE" (LICENSE) for details.

---

❤️ INFINITE CORE

Built for reliable hosting automation, Discord management and local AI-powered infrastructure.
