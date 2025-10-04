import re

from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, "pocetna.html")

def users(request):
    return render(request, "korisnici.html")

def my_page(request):
    return render(request, "moj_profil.html")

def login_page(request):
    return render(request, "login.html")

def signup_page(request):
    return render(request, "signup.html")

def forgot_password(request):
    return render(request, "zaboravljena_lozinka.html")

def become_judge(request):
    return render(request, "postani_ziri.html")