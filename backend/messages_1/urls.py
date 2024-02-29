from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path(r'key/', KeysView.as_view(), name='key'),
    path(r'list/', MessagesListView.as_view(), name='list_message'),
    path(r'create/', MessageCreateView.as_view(), name='create_message'),
]

