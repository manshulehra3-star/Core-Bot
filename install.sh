#!/usr/bin/env bash

set -Eeuo pipefail

# ============================================================
# INFINITE CORE BOT - ONE COMMAND INSTALLER
# ============================================================

REPO_URL="https://github.com/manshulehra3-star/Core-Bot.git"
INSTALL_DIR="/opt/infinite-core-bot"
SERVICE_NAME="infinite-core-bot"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

OLLAMA_MODEL="qwen3.5:0.8b"

echo
echo "============================================================"
echo "        INFINITE CORE BOT - INSTALLER"
echo "============================================================"
echo

# ------------------------------------------------------------
# Root check
# ------------------------------------------------------------

if [[ "${EUID}" -ne 0 ]]; then
    echo "[ERROR] Please run this installer as root."
    echo
    echo "Example:"
    echo "sudo bash install.sh"
    exit 1
fi

# ------------------------------------------------------------
# Detect package manager
# ------------------------------------------------------------

if command -v apt-get >/dev/null 2>&1; then
    export DEBIAN_FRONTEND=noninteractive

    echo "[1/10] Updating system..."
    apt-get update -y
    apt-get upgrade -y

    echo "[2/10] Installing required packages..."
    apt-get install -y \
        python3 \
        python3-venv \
        python3-pip \
        git \
        curl \
        ca-certificates
else
    echo "[ERROR] This installer currently supports Ubuntu/Debian only."
    exit 1
fi

# ------------------------------------------------------------
# Clone / update repository
# ------------------------------------------------------------

echo
echo "[3/10] Installing INFINITE CORE BOT..."

if [[ -d "${INSTALL_DIR}/.git" ]]; then
    echo "Existing installation detected."
    cd "${INSTALL_DIR}"

    git fetch origin
    git reset --hard origin/main
else
    rm -rf "${INSTALL_DIR}"

    git clone "${REPO_URL}" "${INSTALL_DIR}"
    cd "${INSTALL_DIR}"
fi

# ------------------------------------------------------------
# Python virtual environment
# ------------------------------------------------------------

echo
echo "[4/10] Creating Python virtual environment..."

python3 -m venv "${INSTALL_DIR}/venv"

source "${INSTALL_DIR}/venv/bin/activate"

python -m pip install --upgrade pip setuptools wheel

# ------------------------------------------------------------
# Python dependencies
# ------------------------------------------------------------

echo
echo "[5/10] Installing Python dependencies..."

if [[ ! -f "${INSTALL_DIR}/requirements.txt" ]]; then
    echo "[ERROR] requirements.txt not found."
    exit 1
fi

pip install -r "${INSTALL_DIR}/requirements.txt"

# ------------------------------------------------------------
# Create required directories
# ------------------------------------------------------------

mkdir -p "${INSTALL_DIR}/data"

# ------------------------------------------------------------
# Environment file
# ------------------------------------------------------------

echo
echo "[6/10] Preparing environment..."

if [[ ! -f "${INSTALL_DIR}/.env" ]]; then
    if [[ -f "${INSTALL_DIR}/.env.example" ]]; then
        cp "${INSTALL_DIR}/.env.example" "${INSTALL_DIR}/.env"
    else
        touch "${INSTALL_DIR}/.env"
    fi
fi

chmod 600 "${INSTALL_DIR}/.env"

# ------------------------------------------------------------
# Ollama
# ------------------------------------------------------------

echo
echo "[7/10] Installing / configuring Ollama..."

if ! command -v ollama >/dev/null 2>&1; then
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "Ollama already installed."
fi

systemctl enable ollama >/dev/null 2>&1 || true
systemctl restart ollama

echo "Waiting for Ollama..."

OLLAMA_READY=0

for i in {1..30}; do
    if curl -fsS http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
        OLLAMA_READY=1
        break
    fi

    sleep 2
done

if [[ "${OLLAMA_READY}" -ne 1 ]]; then
    echo "[ERROR] Ollama failed to start."
    systemctl status ollama --no-pager || true
    exit 1
fi

echo
echo "Installing AI model: ${OLLAMA_MODEL}"

ollama pull "${OLLAMA_MODEL}"

# ------------------------------------------------------------
# Update AI values in .env
# ------------------------------------------------------------

if grep -q '^AI_ENABLED=' "${INSTALL_DIR}/.env"; then
    sed -i 's/^AI_ENABLED=.*/AI_ENABLED=true/' "${INSTALL_DIR}/.env"
else
    echo "AI_ENABLED=true" >> "${INSTALL_DIR}/.env"
fi

if grep -q '^OLLAMA_HOST=' "${INSTALL_DIR}/.env"; then
    sed -i 's#^OLLAMA_HOST=.*#OLLAMA_HOST=http://127.0.0.1:11434#' "${INSTALL_DIR}/.env"
else
    echo "OLLAMA_HOST=http://127.0.0.1:11434" >> "${INSTALL_DIR}/.env"
fi

if grep -q '^OLLAMA_MODEL=' "${INSTALL_DIR}/.env"; then
    sed -i "s#^OLLAMA_MODEL=.*#OLLAMA_MODEL=${OLLAMA_MODEL}#" "${INSTALL_DIR}/.env"
else
    echo "OLLAMA_MODEL=${OLLAMA_MODEL}" >> "${INSTALL_DIR}/.env"
fi

# ------------------------------------------------------------
# Systemd service
# ------------------------------------------------------------

echo
echo "[8/10] Installing systemd service..."

cat > "${SERVICE_FILE}" <<EOF
[Unit]
Description=INFINITE CORE Discord Bot
After=network-online.target ollama.service
Wants=network-online.target

[Service]
Type=simple
User=root
WorkingDirectory=${INSTALL_DIR}
Environment="PATH=${INSTALL_DIR}/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin"
ExecStart=${INSTALL_DIR}/venv/bin/python ${INSTALL_DIR}/bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

chmod 644 "${SERVICE_FILE}"

systemctl daemon-reload

# ------------------------------------------------------------
# Enable service
# ------------------------------------------------------------

echo
echo "[9/10] Enabling 24/7 bot service..."

systemctl enable "${SERVICE_NAME}"

# ------------------------------------------------------------
# Start bot
# ------------------------------------------------------------

echo
echo "[10/10] Starting INFINITE CORE BOT..."

systemctl restart "${SERVICE_NAME}"

sleep 3

# ------------------------------------------------------------
# Final status
# ------------------------------------------------------------

echo
echo "============================================================"
echo "              INSTALLATION COMPLETE"
echo "============================================================"
echo

if systemctl is-active --quiet "${SERVICE_NAME}"; then
    echo "[SUCCESS] INFINITE CORE BOT is running."
else
    echo "[WARNING] Bot service is not running."
    echo
    echo "Check logs with:"
    echo "journalctl -u ${SERVICE_NAME} -n 100 --no-pager"
fi

echo
echo "Installation directory:"
echo "${INSTALL_DIR}"

echo
echo "Bot status:"
systemctl status "${SERVICE_NAME}" --no-pager || true

echo
echo "============================================================"
echo "IMPORTANT"
echo "============================================================"
echo
echo "Edit your Discord/API configuration:"
echo
echo "nano ${INSTALL_DIR}/.env"
echo
echo "After editing .env, restart the bot:"
echo
echo "systemctl restart ${SERVICE_NAME}"
echo
echo "Live logs:"
echo
echo "journalctl -u ${SERVICE_NAME} -f"
echo
echo "============================================================"
