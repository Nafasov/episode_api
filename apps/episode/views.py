from django.shortcuts import get_object_or_404
from django_filters import rest_framework
from rest_framework import viewsets, generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import filters
from .serializers import (
    TagSerializer,
    CategorySerializer,
    EpisodeSerializer,
    EpisodePOSTSerializer,
    EpisodeCommentSerializer,
    EpisodeLikeSerializer
)
from .models import (
    Category,
    Tag,
    Episode,
    EpisodeComment,
    EpisodeLike
)

from .permission import IsAuthorOrReadOnly
from .filters import EpisodeFilter


class CategoryAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None


class TagAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class EpisodeAPIView(viewsets.ModelViewSet):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    serializer_post_class = EpisodePOSTSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filterset_class = EpisodeFilter
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_serializer_class(self):
        super().get_serializer_class()
        if self.request.method == 'GET':
            return self.serializer_class
        else:
            return self.serializer_post_class


class EpisodeCommentAPIView(generics.ListCreateAPIView):
    # episode/{episode_id}/comment/
    queryset = EpisodeComment.objects.all()
    serializer_class = EpisodeCommentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        episode_id = self.kwargs.get('episode_id')
        context['episode_id'] = episode_id
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        print(self.kwargs.get('episode_id'))
        episode_id = self.kwargs['episode_id']
        if episode_id:
            qs = qs.filter(episode_id=episode_id)
            return qs
        else:
            return qs.none()


class EpisodeCommentDeleteAPIView(generics.DestroyAPIView):
    # episode/{episode_id}/comment/{pk}/
    queryset = EpisodeComment.objects.all()
    serializer_class = EpisodeCommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        episode_id = self.kwargs.get('episode_id')
        if episode_id:
            qs = qs.filter(episode_id=episode_id)
            return qs
        else:
            return qs.none()


class EpisodeLikeAPIView(generics.GenericAPIView):
    # episode/{episode_id}/like/
    queryset = EpisodeLike.objects.all()
    serializer_class = EpisodeLikeSerializer

    def post(self, request, *args, **kwargs):
        episode_id = self.kwargs['episode_id']
        print(request.user)
        user_id = self.request.user.id
        if not user_id:
            raise ValidationError("You are not registered yet")
        print(episode_id, user_id)
        episode = get_object_or_404(Episode, pk=episode_id)
        has_like = EpisodeLike.objects.filter(episode_id=episode_id, author_id=user_id)
        if has_like:
            has_like.delete()
            return Response({'success': True, 'message': 'Episode like remove'})
        else:
            EpisodeLike.objects.create(episode_id=episode.id, author_id=user_id)
            return Response({'success': True, 'message': 'Episode like add'})

