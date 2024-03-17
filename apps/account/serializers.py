from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(min_length=8, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(min_length=8, write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name',  'avatar', 'password1', 'password2', 'created_date']

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')

        if password1 != password2:
            raise ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        password1 = validated_data.pop('password1')
        password2 = validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        user.set_password(password1)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name',  'avatar', 'last_login', 'modified_date', 'created_date']


class ResetPasswordSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True)
    uidb64 = serializers.CharField(max_length=64, required=True)
    token = serializers.CharField(max_length=221, required=True)

    class Meta:
        model = User
        fields = ['password1', 'password2', 'uidb64', 'token']

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        uidb64 = attrs.get('uidb64')
        token = attrs.get('token')
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=user_id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise AuthenticationFailed({'success': False, 'message': 'The reset link is invalid.'})
        if password1 != password2:
            return ValidationError({'success': False, 'message': 'Passwords do not match.'})
        return user

    def create(self, validated_data):
        password1 = validated_data.pop('password1')
        password2 = validated_data.pop('password2')
        uidb64 = validated_data.pop('uidb64')
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=user_id)
        user.set_password(password1)
        user.save()
        return user


            
