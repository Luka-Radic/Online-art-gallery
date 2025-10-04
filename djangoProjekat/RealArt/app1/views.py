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
