from django.urls import path
from . import views

urlpatterns = [
    path('login', views.Login.as_view()),
    path('registration', views.Registration.as_view()),
    path('logout', views.Logout.as_view()),

]