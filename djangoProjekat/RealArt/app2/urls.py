from django.contrib import admin
from django.urls import path, include

from app2 import views

urlpatterns = [
    path('exhibitions/', views.exhibitions, name='exhibitions'),
    path('image_<int:painting_id>/', views.image_detail, name='image_detail'),
]