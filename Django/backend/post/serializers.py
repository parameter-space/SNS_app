from rest_framework import serializers
from .models import Post, Comment
from account.serializers import UserSerializer

# craete를 위한 serializer
class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image = serializers.ImageField(required=False)
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'image', 'author')

# read를 위한 serializer
class PostReadSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    like_list = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'image', 'created_at', 'updated_at', 'like_count', 'comment_count', 'author', 'like_list')
        read_only_fields = ('created_at', 'updated_at', 'like_count', 'comment_count')