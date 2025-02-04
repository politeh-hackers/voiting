from django.http.request import HttpRequest
from django.urls import path
from .views import AppealView, AppealsClientView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', AppealView.as_view()),
    path('<uuid:model_id>', AppealView.as_view()),
    path('appeals', AppealsClientView.as_view())
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
