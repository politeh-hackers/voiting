from django.urls import path
from .views import MediaView, MediaClientView
from django.conf import settings
from django.conf.urls.static import static

# Ваши URL-обработчики
urlpatterns = [
    path('', MediaView.as_view()),  # Обработчик для MediaView
    path('<uuid:model_id>', MediaView.as_view()),  # Обработчик для MediaView с параметром model_id
    path('media', MediaClientView)  # Обработчик для MediaClientView
]

# Настройка обслуживания медиафайлов в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
