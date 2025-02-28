from django.urls import path
from . import views
from .views import Login, Registration, Logout

urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('registration', views.Registration.as_view()),
    path('logout', views.Logout.as_view()),

]