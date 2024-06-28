from rest_framework import serializers
from .models import Post, User, Tag, Category, Comment
from blog_project.settings import Host
from django.contrib.auth.hashers import make_password

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields =('title','image','content','id','category','tag','created_at')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'image', 'id')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # Hash the password
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])  # Hash the updated password
        return super().update(instance, validated_data)
    
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields =('name','id')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields =('name','id')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields =('user','post','content','created_at','id')
