from django.urls import path
from .views import MediaView, MediaClientView

urlpatterns = [
    path('', MediaView.as_view()),
    path('<uuid:model_id>', MediaView.as_view()),
    path('media', MediaClientView)
]