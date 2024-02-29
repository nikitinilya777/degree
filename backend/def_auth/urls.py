from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import (
    RegisterAPI,
    ChangePasswordView,
    ResetPasswordSendMail,
    ResetPasswordVerifyCode,
)

urlpatterns = [
    path(r'api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(r'api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(r'api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path(r'api/v1/registration/', RegisterAPI.as_view(), name='register'),
    path(r'api/v1/change-password/', ChangePasswordView.as_view(), name='change-password'),

    path(r'api/v1/reset-password/send-mail/', ResetPasswordSendMail.as_view(), name='send_mail_reset_password'),
    path(r'api/v1/reset-password/verify-code/', ResetPasswordVerifyCode.as_view(), name='verify_code_reset_password'),
]
