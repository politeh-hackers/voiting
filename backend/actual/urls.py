from django.urls import path
from .views import ActualView, ActualClientView

urlpatterns = [
    path('', ActualView.as_view()),
    path('<uuid:model_id>', ActualView.as_view()),
    path('actual', ActualClientView)
]
