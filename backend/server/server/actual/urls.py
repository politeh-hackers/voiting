from django.urls import path
from .views import ActualView

urlpatterns = [
    path('', ActualView.as_view()),
    path('<uuid:model_id>', ActualView.as_view()),

]
