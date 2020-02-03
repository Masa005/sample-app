from django.contrib.auth import get_user_model
from short_post.models import PostContent
from rest_framework import serializers

User = get_user_model()

class PostContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostContent
        fields = [
            'post_id',
            'content',
            'date_joined',
            'user',
        ]
        depth = 1