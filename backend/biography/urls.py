from django.urls import path
from .views import BiographyClientView, BiographyView

urlpatterns = [
    path('biography', BiographyView.as_view()),
    path('<uuid:model_id>', BiographyView.as_view()),
    path('', BiographyClientView)
]
