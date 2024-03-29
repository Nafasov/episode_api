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
