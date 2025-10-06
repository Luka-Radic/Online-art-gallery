import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User as DjangoUser
from django.shortcuts import render, redirect
from app1.models import User


# Create your views here.
def homepage(request):
    return render(request, "pocetna.html")

def users(request):
    return render(request, "korisnici.html")

def my_page(request):
    return render(request, "moj_profil.html")

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
            if not User.objects.filter(username=username):
                message = 'Ne postoji korisnik sa tim korisnickim imenom'
            else:
                message = "Neispravna lozinka za dato ime."

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
            else:
                user = User.objects.create(username=username, password_hash=password, first_name=name, last_name=lastname,
                                           email=email, bio=description, role='registered', date_joined=None)  # TODO enum
                user.save()
                DjangoUser.objects.create_user(username=username, password=password)
                return redirect("homepage")

    return render(request, "signup.html", {"message": message})

def logout_page(request):
    logout(request)
    return redirect("homepage")

def forgot_password(request):
    return render(request, "zaboravljena_lozinka.html")

def become_judge(request):
    return render(request, "postani_ziri.html")