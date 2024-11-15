from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('media', views.media, name='media'),
    path('biography', views.biography, name='biography'),
    path('appeals', views.appeals, name='appeals'),
]
