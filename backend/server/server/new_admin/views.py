from http import HTTPStatus

from rest_framework import generics
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from typing import Generic, TypeVar
from django.db import models
from base.service import BaseService
from base.views import BaseView
from .models import Post
from .serializers import PostSerializer

class PostListView(APIView):


    def get(self, request):
        queryset = Post.objects.all()  # Указываем queryset
        serializer_class = PostSerializer
        permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

#
# class TestList(APIView):
#     test_service = BaseService(model=Post)
#
#     def get_queryset(self):
#         return Post.objects.get_queryset()
#
#     def get(self, request):
#         return Response(self.test_service.get_all())
#
#     def post(self, request):
#         return Response(BaseService.create())






class TestList(BaseView[Post]):
    model = Post

    def get(self, request):
        return Response(self.get_queryset().values())

    def post(self, request: Request):
        try:
            self.get_queryset().create(**request.data)
            return Response(None, status=HTTPStatus.OK)
        except Exception:
            return Response({"error": "programmer ls sin blyadi"}, status=HTTPStatus.BAD_REQUEST)

