from rest_framework import serializers
from .models import Category, Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post