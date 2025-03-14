from rest_framework import serializers
from .models import News, Tag, Like


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class NewsSerializer(serializers.ModelSerializer):
    tags_list = serializers.SerializerMethodField()
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(), write_only=True)
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'title', 'text', 'picture', 'tags', 'tags_list', 'views', 'created_at', 'dislikes', 'likes']
        read_only_fields = ['id', 'tags_list', 'views',
                            'created_at', 'dislikes', 'likes']

    @staticmethod
    def get_likes(obj):
        return obj.total_likes()

    @staticmethod
    def get_dislikes(obj):
        return obj.total_dislikes()

    @staticmethod
    def get_tags_list(obj):
        return obj.tags.values('name')

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        news = News.objects.create(**validated_data)
        news.tags.set(tags)
        return news


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'session_key', 'news', 'liked', 'created_at']