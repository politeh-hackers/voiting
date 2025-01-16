from django.urls import path
from .views import BiographyView

urlpatterns = [
    path('', BiographyView.as_view()),
    path('<uuid:model_id>', BiographyView.as_view()),

]
