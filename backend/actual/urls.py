from django.urls import path
from .views import ActualView, ActualClientView, ActualCard

urlpatterns = [
    path('', ActualView.as_view()),
    path('<uuid:model_id>', ActualView.as_view()),
    path('actual', ActualClientView),
    path('actual/<uuid:model_id>', ActualCard)
]
