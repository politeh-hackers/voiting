from django.urls import path
from .views import ActualView, ImageView

urlpatterns = [
    path('', ActualView.as_view()),
    path('<uuid:model_id>', ActualView.as_view()),
    
    path('image', ImageView.as_view()),
    path('image/<str:file_name>', ImageView.as_view()),

]
