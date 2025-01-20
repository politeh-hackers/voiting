from django.urls import path
from .views import BiographyClientView, BiographyView

urlpatterns = [
    path('', BiographyView.as_view()),
    path('<uuid:model_id>', BiographyView.as_view()),
    path('biography', BiographyClientView)
]
