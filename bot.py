import requests
import time
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

DEX_URL = "https://api.dexscreener.com/latest/dex/pairs/solana"

seen = set()

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

while True:
    try:
        r = requests.get(DEX_URL, timeout=10).json()
        pairs = r.get("pairs", [])

        for p in pairs:
            pair_id = p.get("pairAddress")
            if not pair_id or pair_id in seen:
                continue

            seen.add(pair_id)

            price = p.get("priceUsd")
            vol = p.get("volume", {}).get("h24")
            name = p.get("baseToken", {}).get("symbol")

            if price and vol and float(vol) > 50000:
                msg = f"🚨 NEW SOL MEME COIN\n\n{name}\n💰 Price: ${price}\n📊 24h Vol: ${vol}"
                send_telegram(msg)

        time.sleep(60)

    except Exception as e:
        print("Error:", e)
        time.sleep(60)
