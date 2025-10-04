
from django.contrib import admin
from django.urls import path, include

import app1, app2, app3
from app1.views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path('users/', users, name='users'),
    path('my_page/', my_page, name='my_page'),
]
