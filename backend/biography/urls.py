from django.urls import path
from .views import BiographyClientView

urlpatterns = [
    path('biography', BiographyClientView)
]