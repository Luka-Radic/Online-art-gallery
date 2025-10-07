import os
import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User as DjangoUser
from django.shortcuts import render, redirect

from RealArt import settings
from app1 import models
from app1.models import User
from enum import Enum

class Role(str, Enum):
    ADMIN = "admin"
    JURY = "jury"
    REGISTERED = "registered"
    GUEST = "guest"


# Create your views here.
def homepage(request):
    return render(request, "pocetna.html")

def users(request):
    users = User.objects.all()
    return render(request, "korisnici.html", {"users": users})

def my_page(request):
    username = request.user.username
    me = User.objects.filter(username=username).first()
    if not me: redirect("homepage")
    return render(request, "moj_profil.html", {"me": me})

def artist(request, id):
    user = User.objects.filter(id=id).first()
    if not user: redirect("homepage")
    return render(request, "umetnik.html", {"user": user})

def login_page(request):
    if request.user.is_authenticated:
        return redirect("homepage")
    message = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            print("Ulogovan")
            return redirect('homepage')
        else:
            input = {}
            if not User.objects.filter(username=username):
                message = 'Ne postoji korisnik sa tim korisnickim imenom'
                input["password"] = password
            else:
                message = "Neispravna lozinka za dato ime."
                input["username"] = username

        return render(request, "login.html", {"message": message, "input": input})

    return render(request, "login.html", {"message": message})


def signup_page(request):
    message = ""
    if request.method == "POST":
        name = request.POST.get("ime")
        lastname = request.POST.get("prezime")
        username = request.POST.get("korisnickoIme")
        password = request.POST.get("lozinka")
        password_again = request.POST.get("potvrdaLozinke")
        email = request.POST.get("email")
        description = request.POST.get("opis")
        state = request.POST.get("drzava")

        if password != password_again:
            message = "Sifre se ne podudaraju."

        else:
            if User.objects.filter(username=username):
                message = "Korisnik sa tim korisnickim imenom vec postoji. Unesite drugo."
            elif User.objects.filter(email=email):
                message = "Korisnik sa tim email-om vec postoji."
            else:
                user = User.objects.create(username=username, password_hash=password, first_name=name, last_name=lastname,
                                           email=email, bio=description, role=Role.REGISTERED, date_joined=None)
                user.save()
                django_user = DjangoUser.objects.create_user(username=username, password=password)
                login(request, django_user)
                return redirect("homepage")

    return render(request, "signup.html", {"message": message})

def logout_page(request):
    logout(request)
    return redirect("homepage")

def forgot_password(request):
    return render(request, "zaboravljena_lozinka.html")

def become_judge(request):
    return render(request, "postani_ziri.html")\

def search_users(request):
    users = User.objects.all()
    input= ""
    filtered = None
    if request.method == "POST":
        input = request.POST.get("search")
        if input != "":
            filtered = list(users.filter(username__icontains=input))
            filtered += list(users.filter(first_name__icontains=input))
            filtered += list(users.filter(last_name__icontains=input))
            filtered = set(filtered)

    return render(request, "korisnici.html", {"users": users, "filtered": filtered, "input": input})


def add_pfp_page(request):
    return render(request, "dodaj_proflnu.html")

def add_pfp(request):
    print("usao")
    djuser = request.user
    print (djuser.username)
    user = User.objects.filter(username=djuser.username).first()
    if request.method == "POST" and request.FILES.get('image') is not None:
        image = request.FILES.get("image")
        print(image)
        if image.content_type.startswith('image/'):
            base, ext = os.path.splitext(image.name)
            filename = f'{djuser.username}{ext}'
            print(filename)
            path = os.path.join(settings.BASE_DIR,'static', 'img', filename)

            with open(path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            image_url = f'/static/img/{filename}'
            user.pfp_url = image_url
            user.save()
    return render(request, 'moj_profil.html', {"me":user})



def delete_profile(request):
    username = request.user.username
    User.objects.filter(username=username).delete()
    DjangoUser.objects.filter(username=username).delete()
    return redirect("homepage")
