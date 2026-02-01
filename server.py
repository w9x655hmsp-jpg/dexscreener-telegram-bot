from flask import Flask, request
import requests
import os

app = Flask(__name__)

# ENV VARIABLES (you will set these on Render later)
TELEGRAM_BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("CHAT_ID")

TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

def send_telegram_message(text):
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(TELEGRAM_URL, json=payload)

@app.route("/", methods=["GET"])
def home():
    return "Dexscreener Telegram Bot is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    # Example fields from Dexscreener-style alerts
    pair = data.get("pair", "Unknown Pair")
    price = data.get("priceUsd", "N/A")
    volume = data.get("volume", "N/A")
    chain = data.get("chain", "Solana")

    message = (
        f"🚨 <b>New Dex Alert</b>\n\n"
        f"🪙 Pair: {pair}\n"
        f"💰 Price: ${price}\n"
        f"📊 Volume: {volume}\n"
        f"⛓ Chain: {chain}"
    )

    send_telegram_message(message)
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
