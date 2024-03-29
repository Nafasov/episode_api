from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response

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


class CategoryAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class EpisodeAPIView(viewsets.ModelViewSet):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    serializer_post_class = EpisodePOSTSerializer
    permission_classes = [IsAuthorOrReadOnly]

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
    permission_classes = [IsAuthorOrReadOnly]

    def get_serializer_context(self, **kwargs):
        ctx = super().get_serializer_class()
        episode_id = self.kwargs['episode_id']
        ctx['episode_id'] = episode_id
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()
        episode_id = self.kwargs['episode_id']
        if episode_id:
            qs = qs.filter(episode_id=episode_id)
        else:
            return qs.none()


class EpisodeCommentDeleteAPIView(generics.DestroyAPIView):
    # episode/{episode_id}/comment/{pk}/
    queryset = EpisodeComment.objects.all()
    serializer_class = EpisodeCommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        episode_id = self.kwargs['episode_id']
        if episode_id:
            qs = qs.filter(episode_id=episode_id)
        else:
            return qs.none()


class EpisodeLikeAPIView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        episode_id = self.kwargs['episode_id']
        user_id = self.request.user.id
        has_like = EpisodeLike.objects.filter(episode_id=episode_id, author_id=user_id)
        if has_like:
            has_like.delete()
            return Response({'success': True, 'message': 'Episode like remove'})
        else:
            EpisodeLike.objects.create(episode_id=episode_id, author_id=user_id)
            return Response({'success': True, 'message': 'Episode like add'})
