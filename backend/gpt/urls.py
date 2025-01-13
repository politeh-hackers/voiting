from django.urls import path
from gpt.views import generate

urlpatterns = [
    path('generate', generate)
]
