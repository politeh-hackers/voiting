from django.urls import path
from .views import CategoryView

urlpatterns = [
    path('', CategoryView.as_view()),
    path('<uuid:model_id>', CategoryView.as_view()),
]