from django.urls import path
from .views import AppealView

urlpatterns = [
    path('', AppealView.as_view()),
    path('/<uuid:model_id>', AppealView.as_view()),

]
