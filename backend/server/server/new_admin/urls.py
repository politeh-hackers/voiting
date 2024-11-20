from django.urls import path
from .views import PostListView, TestList, TestId, TestMediaTag

urlpatterns = [
    path('', TestMediaTag.as_view(), name='post-list'),
    path('<int:test_id>', TestId.as_view())
]
