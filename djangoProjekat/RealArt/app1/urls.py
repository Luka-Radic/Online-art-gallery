
from django.contrib import admin
from django.urls import path, include


from app1.views import *
from app2.views import image_detail

urlpatterns = [
    path('', homepage, name='homepage'),
    path('users/', users, name='users'),
    path('my_page/', my_page, name='my_page'),
    path('artist/<int:id>', artist, name='artist'),
    path('login/', login_page, name='login_page'),
    path('signup/', signup_page, name='signup_page'),
    path('logout/', logout_page, name='logout_page'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('become_judge', become_judge, name='become_judge'),
    path ('search_users', search_users, name='search_users'),
    path('delete_profile/', delete_profile, name='delete_profile'),
    path('add_pfp/', add_pfp, name='add_pfp'),
    path('add_pfp_page/', add_pfp_page, name='add_pfp_page'),

    path('image<int:painting_id>/', image_detail, name='image_detail'),

]
