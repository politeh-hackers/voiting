from django.urls import path
from .views import MediaView

urlpatterns = [
    path('', MediaView.as_view()),
    path('<uuid:model_id>', MediaView.as_view()),
]