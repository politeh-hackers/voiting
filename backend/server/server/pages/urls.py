from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('admin', views.admin, name='admin'),
    path('admin/category', views.CategoryView),
    path('admin/media', views.MediaView),

]
