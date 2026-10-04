🚀 INFINITE CORE BOT

<p align="center">
  <b>Production-Grade Discord Automation for Hosting, Payments, Tickets & Local AI</b>
</p><p align="center">
  ⚡ Fast &nbsp;•&nbsp; 🤖 AI Powered &nbsp;•&nbsp; 🔐 Secure &nbsp;•&nbsp; ♾️ 24/7
</p><p align="center">"Python" (https://img.shields.io/badge/Python-3.10%2B-blue)
"Discord.py" (https://img.shields.io/badge/discord.py-2.3%2B-5865F2)
"Ollama" (https://img.shields.io/badge/AI-Ollama-black)
"License" (https://img.shields.io/badge/License-MIT-yellow)

</p>---

🌐 Official Repository

INFINITE CORE BOT

GitHub:
https://github.com/manshulehra3-star/Core-Bot

---

✨ Features

┌──────────────────────────────────────────────────┐
│              🚀 INFINITE CORE BOT                │
├──────────────────────────────────────────────────┤
│                                                  │
│  🤖 Discord Automation                           │
│  🎫 Advanced Ticket System                       │
│  💳 Payment Management                           │
│  🖥️ VPS / Hosting Integration                    │
│  🎮 Minecraft Panel Integration                  │
│  🧠 Local AI with Ollama                         │
│  🗄️ SQLite Database                              │
│  🔄 GitHub Update Support                        │
│  ♾️ 24/7 Systemd Service                         │
│  🔥 Automatic Restart                            │
│  ⚡ Auto Start After VPS Reboot                  │
│                                                  │
└──────────────────────────────────────────────────┘

---

🖥️ Requirements

Supported Operating Systems

- Ubuntu 22.04 LTS
- Ubuntu 24.04 LTS
- Debian 12

Recommended Hardware

CPU      : 8+ vCPU
RAM      : 16–32 GB
Storage  : SSD / NVMe
Python   : 3.10+

«💡 Local AI inference performance depends on your VPS hardware and selected Ollama model.»

---

⚡ ONE-COMMAND INSTALLATION

🚀 Install Everything Automatically

The repository includes an automated "install.sh" installer.

You do not need to manually install Python, pip, Git, Ollama, dependencies or systemd.

Simply copy the command below and run it on your VPS:

```curl -fsSL https://raw.githubusercontent.com/manshulehra3-star/Core-Bot/main/install.sh | sudo bash```

🛠️ The installer automatically handles

① System package update
        ↓
② Python installation
        ↓
③ Python virtual environment
        ↓
④ Git & required packages
        ↓
⑤ INFINITE CORE BOT download
        ↓
⑥ Python dependencies
        ↓
⑦ Ollama installation
        ↓
⑧ Local AI model installation
        ↓
⑨ .env preparation
        ↓
⑩ Systemd service
        ↓
⑪ 24/7 bot service
        ↓
⑫ Automatic startup after reboot

✅ After installation

Configure your credentials:

```nano /opt/infinite-core-bot/.env```

Then restart:

```systemctl restart infinite-core-bot```

---

🧠 LOCAL AI

INFINITE CORE BOT uses Ollama for local AI inference.

Default model

qwen3.5:0.8b

Check Ollama:

```ollama --version```

Check installed models:

```ollama list```

Check Ollama service:

```systemctl status ollama```

---

⚙️ ENVIRONMENT CONFIGURATION

Your configuration file is located at:

```/opt/infinite-core-bot/.env```

Open it:

```nano /opt/infinite-core-bot/.env```

Configure your:

Discord Bot Token
Owner ID
Guild ID

Welcome Channel
Leave Channel

Ticket Category
Ticket Logs

Payment Logs
Payment Owner

Ollama configuration

SVM / VPS Panel API
Minecraft Panel API

🔐 Security Warning

Never publish your ".env" file.

It may contain:

- Discord Bot Token
- API Keys
- Panel Credentials
- Private configuration

---

♾️ 24/7 SERVICE

The installer automatically configures a systemd service.

The bot will:

✅ Run continuously
✅ Restart automatically if it crashes
✅ Start automatically after VPS reboot

Check status

```systemctl status infinite-core-bot```

Start

```systemctl start infinite-core-bot```

Stop

```systemctl stop infinite-core-bot```

Restart

```systemctl restart infinite-core-bot```

Enable on boot

```systemctl enable infinite-core-bot```

---

📋 LIVE LOGS

View live bot logs:

```journalctl -u infinite-core-bot -f```

View the latest 100 logs:

```journalctl -u infinite-core-bot -n 100 --no-pager```

View Ollama logs:

```journalctl -u ollama -n 100 --no-pager```

---

🔄 UPDATE

Update the bot from GitHub:

```cd /opt/infinite-core-bot && systemctl stop infinite-core-bot && git pull origin main && source venv/bin/activate && pip install -r requirements.txt --upgrade && systemctl restart infinite-core-bot```

After updating, check:

```systemctl status infinite-core-bot```

---

🩺 HEALTH CHECK

Check the bot:

```systemctl is-active infinite-core-bot```

Check Ollama:

```systemctl is-active ollama```

Check Ollama API:

```curl -fsS http://127.0.0.1:11434/api/tags```

Check Python:

```python3 --version```

---

🗂️ INSTALLATION DIRECTORY

The bot is installed at:

/opt/infinite-core-bot

Typical structure:

/opt/infinite-core-bot/
│
├── bot.py
├── requirements.txt
├── .env
├── .env.example
├── infinite-core-bot.service
│
├── data/
│   └── infinite_core.db
│
└── venv/

---

🔐 SECURITY

Add the following to ".gitignore":

.env
*.db
*.sqlite
*.sqlite3
venv/
.venv/
__pycache__/
*.pyc

❌ Never upload

.env
Discord tokens
API keys
Private keys
Database files containing sensitive data

---

🛠️ TROUBLESHOOTING

Bot is not starting

Run:

```systemctl status infinite-core-bot```

Then:

```journalctl -u infinite-core-bot -n 100 --no-pager```

---

```Ollama is not working```

Restart:

```systemctl restart ollama```

Check:

```systemctl status ollama```

Test:

```curl http://127.0.0.1:11434/api/tags```

---

AI model is missing

Check:

```ollama list```

Install the default model:

```ollama pull qwen3.5:0.8b```

Then:

```systemctl restart infinite-core-bot```

---

📌 QUICK COMMANDS

Action| Command
🚀 Start| "systemctl start infinite-core-bot"
⛔ Stop| "systemctl stop infinite-core-bot"
🔄 Restart| "systemctl restart infinite-core-bot"
📊 Status| "systemctl status infinite-core-bot"
📋 Logs| "journalctl -u infinite-core-bot -f"
🧠 Ollama| "systemctl status ollama"
🤖 AI Models| "ollama list"

---

📜 LICENSE

This project is licensed under the MIT License.

See the "LICENSE" file for details.

---

💙 INFINITE CORE

<p align="center">POWERFUL AUTOMATION. ZERO LIMITS.

Built for modern hosting infrastructure, Discord automation & local AI.

</p>---

<p align="center">
  ⭐ Star the repository if you find it useful!
</p>
