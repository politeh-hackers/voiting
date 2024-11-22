from django.urls import path, include
from . import views
from .views import CategoryView

urlpatterns = [
    path('', views.home, name='home'),
    path('admin', views.admin, name='admin'),
    path('admin/category', CategoryView.as_view()),
    path('admin/category/<uuid:model_id>', CategoryView.as_view(), name='category_delete'),
    path('admin/media', views.MediaView),

]
