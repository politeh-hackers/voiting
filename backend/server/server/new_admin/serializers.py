from rest_framework import serializers
from .models import Post
from pages.models import MediaTag

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaTag
        fields = '__all__'
