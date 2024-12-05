from django.urls import path, include
from . import views

urlpatterns = [
    path('/login', views.Login.as_view()),
    path('/registation', views.Registration.as_view()),

]