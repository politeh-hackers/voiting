from django.urls import path
from . import views
from .views import MediaView, ImageView

urlpatterns = [
    path('', MediaView.as_view()),
    path('/<uuid:model_id>', MediaView.as_view()),

    path('/image', ImageView.as_view()),
    path('/image/<str:file_name>', ImageView.as_view()),
]