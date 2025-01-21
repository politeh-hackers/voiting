from django.urls import path
from .views import TelegramNotificationView

urlpatterns = [
    path('send_news/', TelegramNotificationView.as_view(), name='send_news'),
]
