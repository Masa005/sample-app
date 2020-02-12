from django.contrib.auth import get_user_model
from short_post.models import PostContent
from rest_framework import serializers
from short_post.models import Favorite

User = get_user_model()


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = [
            'favorite_id',
            'post_content',
            'user',
            'date_joined',
        ]
        depth = 1


class PostContentSerializer(serializers.ModelSerializer):
    prefetch_favorite = FavoriteSerializer(many=True)

    class Meta:
        model = PostContent
        fields = [
            'post_id',
            'content',
            'date_joined',
            'user',
            'prefetch_favorite',
        ]
        depth = 1