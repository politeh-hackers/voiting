from django.urls import path
from .views import ActualView, ActualClientView, ActualCard

urlpatterns = [
    path('actual', ActualView.as_view()),
    path('<uuid:model_id>', ActualView.as_view()),
    path('', ActualClientView),
    path('<slug:slug>', ActualCard),
]
