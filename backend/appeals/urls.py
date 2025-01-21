from django.http.request import HttpRequest
from django.urls import path
from .views import AppealView, AppealsClientView

urlpatterns = [
    path('', AppealView.as_view()),
    path('<uuid:model_id>', AppealView.as_view()),
    path('appeals', AppealsClientView.as_view())
]
