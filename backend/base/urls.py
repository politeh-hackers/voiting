from django.urls import path
from base.views import MainClientView

urlpatterns = [
    
    path('MainPage', MainClientView)
]
