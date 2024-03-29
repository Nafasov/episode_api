from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryAPIView,
    TagAPIView,
    EpisodeAPIView,
    EpisodeCommentAPIView,
    EpisodeCommentDeleteAPIView,
    EpisodeLikeAPIView
)

app_name = 'episode'

router = DefaultRouter()
router.register('actions', EpisodeAPIView)


urlpatterns = [
    path('category/', CategoryAPIView.as_view()),
    path('tag/', TagAPIView.as_view()),
    path('<int:episode_id>/comment/', EpisodeCommentAPIView.as_view()),
    path('<int:episode_id>/comment/<int:pk>/', EpisodeCommentDeleteAPIView.as_view()),
    path('<int:episode_id>/like/', EpisodeLikeAPIView.as_view()),
    path('', include(router.urls))
]


"""

    Tag
    -list
    
    Category
    -list
    
    Episode
    -list
    -detail
    -create
    -update
    -delete
    
    Comment
    -list
    -create
    -delete
    
    EpisodeLike
    -like
    -dislike
    
"""