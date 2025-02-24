from django.http.request import HttpRequest
from django.urls import path
from .views import AppealCard, AppealView, AppealsClientView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('appeals', AppealView.as_view()),
    path('<uuid:model_id>', AppealView.as_view()),
    path('', AppealsClientView.as_view()),
    path('<slug:slug>', AppealCard)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
