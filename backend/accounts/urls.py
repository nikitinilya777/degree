from django.urls import path
from .views import *

urlpatterns = [
    path(r'registration/', RegistrationAPIView.as_view(), name='account-create'),
    path(r'login/', LoginAPIView.as_view(), name='login')
]
