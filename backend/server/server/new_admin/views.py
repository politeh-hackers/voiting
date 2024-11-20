from http import HTTPStatus
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from base.views import BaseView
from .models import Post
from .schemas import MediaTagSchema
from .serializers import PostSerializer
from pages.models import MediaTag

class PostListView(APIView):

    def get(self, request):
        queryset = Post.objects.all()  # Указываем queryset
        serializer_class = PostSerializer
        permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


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

class TestMediaTag(BaseView[MediaTag]):
    model = MediaTag

    def get(self, request):
        return Response(self.get_queryset().values())

    def post(self, request: Request):
        try:
            self.get_queryset().create(**request.data)
            return Response(None, status=HTTPStatus.OK)
        except Exception:
            return Response({"error": "programmer ls sin blyadi"}, status=HTTPStatus.BAD_REQUEST)

class TestId(BaseView[MediaTag]):
    model = MediaTag

    def get(self, request: Request, test_id: int):
        data: MediaTag = self.get_queryset().get(id=test_id)
        return Response(MediaTagSchema(
            id=data.id,
            name=data.name,
        ))

    def delete(self, request: Request, test_id: int):
        try:
            self.get_queryset().get(id=test_id).delete()
            return Response(None, status=HTTPStatus.OK)
        except Exception:
            return Response({"error": "programmer ls sin blyadi"}, status=HTTPStatus.BAD_REQUEST)
