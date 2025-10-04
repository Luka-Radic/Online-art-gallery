
from django.contrib import admin
from django.urls import path, include


from app1.views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path('users/', users, name='users'),
    path('my_page/', my_page, name='my_page'),
    path('login/', login_page, name='login_page'),
    path('signup/', signup_page, name='signup_page'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('become_judge', become_judge, name='become_judge'),
]
