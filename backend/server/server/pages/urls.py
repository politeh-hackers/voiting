from django.urls import path, include
from . import views
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/media', views.MediaView.as_view()),
    path('admin/media/<uuid:model_id>', views.MediaView.as_view()),
    
    path('admin/image', ImageView.as_view()),
    path('admin/image/<str:file_name>', ImageView.as_view()),

    path('admin/actual', ActualView.as_view()),
    path('admin/actual/<uuid:model_id>', ActualView.as_view()),

    path('admin/category', CategoryView.as_view()),
    path('admin/category/<uuid:model_id>', CategoryView.as_view()),

    path('admin/appeal', AppealView.as_view()),
    path('admin/appeal/<uuid:model_id>', AppealView.as_view()),

]
