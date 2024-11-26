from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name='home'),

    path('admin/media', views.MediaView.as_view()),
    path('admin/media/<uuid:model_id>', views.MediaView.as_view()),

    path('admin/actual', ActualView.as_view()),
    path('admin/actual/<uuid:model_id>', ActualView.as_view()),

    path('admin/category', CategoryView.as_view()),
    path('admin/category/<uuid:model_id>', CategoryView.as_view()),

    path('admin/appeal', AppealView.as_view()),
    path('admin/appeal/<uuid:model_id>', AppealView.as_view()),

]
