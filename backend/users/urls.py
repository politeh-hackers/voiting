from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login', views.Login.as_view()),
    path('refresh', TokenRefreshView.as_view()),
    path('registration', views.Registration.as_view()),
    path('logout', views.Logout.as_view()),

]