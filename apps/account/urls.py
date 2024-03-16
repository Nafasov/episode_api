from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)

from .views import (
    UserRegisterAPIView,

)


app_name = 'account'


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_refresh'),
    path('api/token/black/list/', TokenBlacklistView.as_view(), name='black_list'),
    path('api/user/register/', UserRegisterAPIView.as_view(), name='register_user'),
]
