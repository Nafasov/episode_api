from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)

from .views import (
    UserRegisterAPIView,
    MyProfileAPIView,
    ResetPasswordAPIView,
    PasswordTokenCheckAPIView,
    SetPasswordAPIView
)


app_name = 'account'


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_refresh'),
    path('api/token/black/list/', TokenBlacklistView.as_view(), name='black_list'),
    path('api/user/register/', UserRegisterAPIView.as_view(), name='register_user'),
    path('api/user/profile/', MyProfileAPIView.as_view(), name='profile'),
    path('api/user/reset-password/', ResetPasswordAPIView.as_view(), name='reset_password'),
    path('api/user/password-token/<str:uidb64>/<str:token>/', PasswordTokenCheckAPIView.as_view(), name='check_password'),
    path('api/user/set-password/', SetPasswordAPIView.as_view(), name='set_password')


]
