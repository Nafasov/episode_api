from rest_framework import serializers

from .models import (
    Category,
    Tag,
    Episode,
    EpisodeComment,
    EpisodeLike
)
from apps.account.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']


class EpisodeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Episode
        fields = ['id', 'title', 'slug', 'category', 'tags', 'author', 'image', 'music', 'description', 'created_date']


class EpisodePOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['id', 'title', 'slug', 'category', 'tags', 'author', 'image', 'music', 'description']

    def create(self, validated_data):
        request = self.context['request']
        author_id = request.user.id
        validated_data['author_id'] = author_id
        return super().create(validated_data)


class EpisodeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EpisodeComment
        fields = ['id', 'comment', 'parent', 'top_level_comment_id']
        red_only_fields = ['top_level_comment_id']

    def create(self, validated_data):
        request = self.context['request']
        episode_id = self.context['episode_id']
        author_id = request.user.id
        validated_data['author_id'] = author_id
        validated_data['episode_id'] = episode_id
        return super().create(validated_data)


class EpisodeLikeSerializer(serializers.Serializer):
    pass
    # def create(self, validated_data):
    #     request = self.context['request']
    #     episode_id = self.context['episode_id']
    #     user_id = request.user.id
    #     validated_data['episode_id'] = episode_id
    #     validated_data['user_id'] = user_id
    #     super().create(**validated_data)
    #     return validated_data
