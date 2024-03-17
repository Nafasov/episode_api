from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import  smart_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .tasks import send_mail_reset_password

from .serializers import (
    UserRegisterSerializer,
    UserSerializer,
    ResetPasswordSerializer,
    SetNewPasswordSerializer
)
from .models import User


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class MyProfileAPIView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class ResetPasswordAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        print(request.data)
        email = request.data.get("email")
        print(email)
        user_id = get_object_or_404(User, email=email).id
        print(user_id)
        send_mail_reset_password.apply_async((user_id, ))
        ctx = {
            'success': True,
            'message': 'Send email has been reset'
        }
        return Response(ctx)


class PasswordTokenCheckAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message': 'Token is not valid'}, status=406)
            return Response({'message': 'Successfully checked',
                             'uidb64': uidb64,
                             'token': token},
                              status=401)
        except Exception as e:
            return Response({'success': False,
                            'message': f'Token is not valid, please try again new | {e.args}'},
                            status=401)


class SetPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'success': True, 'message': 'Successfully Password Changed'})

