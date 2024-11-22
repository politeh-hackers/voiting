from django.urls import path, include
from . import views
from .views import CategoryView

urlpatterns = [
    path('', views.home, name='home'),

    path('admin/media', views.MediaView),
    path('admin/media/<uuid:model_id>', views.MediaView),
    path('admin/category', CategoryView.as_view()),
    path('admin/category/<uuid:model_id>', CategoryView.as_view()),
    path('admin/settings/new', AdminsView.as_view()),

]
