from django.shortcuts import render
from rest_auth.registration.views import RegisterView
from .models import User


class CustomRegisterView(RegisterView):
    queryset = User.objects.all()
