import requests
from django.conf import settings

TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
TELEGRAM_CHANNEL_ID = settings.TELEGRAM_CHANNEL_ID

def send_news_to_telegram(header, summary, main_photo, url):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    message = f"__{header}__\n\n_{summary}_\n\n[Подробнее]({url})"
    data = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "caption": message,  
        "parse_mode": "Markdown"
    }
    with open(main_photo, 'rb') as photo_file:
        files = {
            "photo": photo_file 
        }
        response = requests.post(api_url, data=data, files=files)   
    return response.json()

def send_appeal_to_telegram(category, date, url):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    message = f"__Обращение__ _{category}_ от _{date}_ __ИСПОЛНЕНО__\n\n[Подробнее]({url})"
    data = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "caption": message,  
        "parse_mode": "Markdown"
    }
    response = requests.patch(api_url, data=data)
    return response.json()