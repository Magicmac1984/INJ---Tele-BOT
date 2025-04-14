from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Telegram bot credentials
TELEGRAM_BOT_TOKEN = "7752803737:AAH7YQzMh_gH36p_WyIEiKAWTo86XmU3NMg"
TELEGRAM_CHAT_ID = "6847513148"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    return response.json()

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    # Basic expected fields from TradingView
    symbol = data.get("symbol", "N/A")
    signal_type = data.get("type", "Signal")
    price = data.get("price", "N/A")
    strategy = data.get("strategy", "N/A")
    timestamp = data.get("time", "N/A")

    # Format the message
    message = f"\ud83d\udcc9 *{signal_type.upper()} Signal* for *{symbol}*\n" \
              f"*Price:* ${price}\n" \
              f"*Strategy:* {strategy}\n" \
              f"*Time:* {timestamp}"

    # Send message
    send_telegram_message(message)

    return {"status": "ok"}, 200

@app.route("/")
def index():
    return "Telegram bot for INJ signals is running."

if __name__ == "__main__":
    app.run(debug=True)
