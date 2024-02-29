from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django_rest_passwordreset.signals import (
    reset_password_token_created,
    pre_password_reset,
    post_password_reset
)
from django_rest_passwordreset.models import ResetPasswordToken
from rest_framework import exceptions

from django.conf import settings
from django.contrib.auth.password_validation import validate_password, get_password_validators

from .serializers import (
    UserSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
    ResetPasswordSendMailSerializer,
    ResetPasswordVerifyCodeSerializer,
)

import re
from datetime import datetime


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
        })


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated, ]

    def get_object(self, queryset=None):
        return self.request.user


HTTP_USER_AGENT_HEADER = getattr(settings, 'DJANGO_REST_PASSWORDRESET_HTTP_USER_AGENT_HEADER', 'HTTP_USER_AGENT')
HTTP_IP_ADDRESS_HEADER = getattr(settings, 'DJANGO_REST_PASSWORDRESET_IP_ADDRESS_HEADER', 'REMOTE_ADDR')


class ResetPasswordSendMail(generics.CreateAPIView):
    serializer_class = ResetPasswordSendMailSerializer
    model = User

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=serializer.validated_data['email'])

        token = ResetPasswordToken.objects.create(
            user=user,
            user_agent=request.META.get(HTTP_USER_AGENT_HEADER, ''),
            ip_address=request.META.get(HTTP_IP_ADDRESS_HEADER, ''),
        )
        reset_password_token_created.send(sender=self.__class__, request=self, reset_password_token=token)

        context = {
            'username': token.user.username,
            'email': token.user.email,
        }
        email_plaintext_message = f"Код для востановления: {token.key}"

        send_mail(
            # title:
            "Password Reset for {title}".format(title="Some website title"),
            # message:
            email_plaintext_message,
            # from:
            'nikitinilya777@gmail.com',
            # to:
            [token.user.email]
        )
        return Response({'Succes': True})


class ResetPasswordVerifyCode(generics.GenericAPIView):
    serializer_class = ResetPasswordVerifyCodeSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data['password']
        token = serializer.validated_data['token']

        reset_password_token = ResetPasswordToken.objects.filter(key=token).first()

        if reset_password_token.user.eligible_for_reset():
            pre_password_reset.send(
                sender=self.__class__,
                user=reset_password_token.user,
                reset_password_token=reset_password_token,
            )
            try:
                validate_password(
                    password,
                    user=reset_password_token.user,
                    password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
                )
            except ValidationError as e:
                raise exceptions.ValidationError({
                    'password': e.messages
                })

            reset_password_token.user.set_password(password)
            reset_password_token.user.save()
            post_password_reset.send(
                sender=self.__class__,
                user=reset_password_token.user,
                reset_password_token=reset_password_token,
            )

        ResetPasswordToken.objects.filter(user=reset_password_token.user).delete()

        return Response({'Succes': True})
