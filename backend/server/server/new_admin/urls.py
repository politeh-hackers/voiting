from django.urls import path
from .views import PostListView, TestList

urlpatterns = [
    path('', TestList.as_view(), name='post-list'),
]
