from djoser.serializers import UserCreateSerializer


from rest_framework import serializers
from django.contrib.auth import get_user_model
User=get_user_model()
from .models import Post, Comment, LikedPost

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer):
        model=User
        fields=['id','email','name','password','is_verified']

        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','first_name','last_name','profile_picture']

class verifier(serializers.Serializer):
    id=serializers.EmailField()
    
class postSerializer(serializers.ModelSerializer):
    poster=UserSerializer(read_only=True)
    class Meta:
        model=Post
        fields="__all__"

class commentSerializer(serializers.ModelSerializer):
    replies=serializers.StringRelatedField(many=True)
    commented_by=UserSerializer()
    class Meta:
        model=Comment
        fields="__all__"

class LikedPostSerializer(serializers.ModelSerializer):
    liked_by=UserSerializer(read_only=True)
    liked_post=postSerializer(read_only=True)
    class Meta:
        model=LikedPost
        fields="__all__"