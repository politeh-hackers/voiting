import json
import logging
from django.http import JsonResponse
from django.views import View
from .bot import send_news_to_telegram

# Настроим логирование
logger = logging.getLogger(__name__)

class TelegramNotificationView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            title = data.get("title")
            description = data.get("description")
            main_photo = data.get("main_photo")
            url = data.get("url")

            # Логирование полученных данных
            logger.info(f"Получены данные: {data}")

            if not title or not description or not url:
                return JsonResponse({"error": "Invalid data"}, status=400)

            response = send_news_to_telegram(title, description, main_photo, url)

            # Логирование ответа от Telegram API
            logger.info(f"Ответ от Telegram: {response}")

            return JsonResponse({"message": "Sent to Telegram", "response": response}, status=200)

        except Exception as e:
            logger.error(f"Ошибка при обработке запроса: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
