import os
import requests
from django.conf import settings

TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
TELEGRAM_CHANNEL_ID = settings.TELEGRAM_CHANNEL_ID

def send_news_to_telegram(title, description, url):
    """Отправляет новость в Telegram-канал"""
    message = f"📰 *{title}*\n\n{description}\n\nПодробнее: {url}"
    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": message,
        "parse_mode": "Markdown",
    }

    response = requests.post(api_url, data=data)
    return response.json()
