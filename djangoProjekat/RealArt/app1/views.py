import os
import requests

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User as DjangoUser
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string

from RealArt import settings
from app1.models import User, Painting, Funding, Juryrequest
from enum import Enum


PAYPAL_CLIENT_ID = "ATCPLO9nK8__yOvaqljL-aYPsiNZhhEXSSCUOkgU8wtZpr_ETaRtaCXoEOfFEC3I6TG1RZvVqJ7fH0vn" #client id
PAYPAL_SECRET = "EFJrsC_qq6kuQIT_-ar2uJzi4j7GTeHO9Bm6DEcSyLhPlKXFxA6nHgaAQ1ODoNf_pdnaizaPAa1_vUbO" #secret key1
PAYPAL_API = "https://api-m.sandbox.paypal.com"

class Role(str, Enum):
    '''
    Enum for user roles.
    '''
    ADMIN = "admin"
    JURY = "jury"
    REGISTERED = "registered"
    GUEST = "guest"


# Create your views here.
def homepage(request):
    '''
    Renders the homepage.
    '''
    return render(request, "pocetna.html")

def users(request):
    '''
    Renders the users page. Fetches and displays all users.
    '''
    users = User.objects.all()
    return render(request, "korisnici.html", {"users": users})

def my_page(request):
    '''
    Renders the profile page of the logged-in user.
    If the user is not found, redirects to the homepage.
    There's ability to edit the page.
    Also fetches and displays their info and the paintings created by the user.
    '''
    username = request.user.username
    me = User.objects.filter(username=username).first()
    if me is None: redirect("homepage")
    paintings = Painting.objects.filter(artist_id=me.id)
    return render(request, "moj_profil.html", {"me": me, "paintings": paintings})

def artist(request, id):
    '''
    Renders the profile page of a specific artist by their id.
    If the artist is not found, redirects to the homepage. 
    Also fetches and displays their info and paintings created by the artist.
    '''
    user = User.objects.filter(id=id).first()
    if not user: redirect("homepage")
    paintings = Painting.objects.filter(artist_id=id)
    return render(request, "umetnik.html", {"user": user, "paintings": paintings})

def login_page(request):
    '''
    Renders the login page and handles user authentication. 
    If the user is already authenticated, redirects to the homepage.
    If successful, logs user in.
    If authentication fails, it provides appropriate error messages.
    '''
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
    '''
    Renders the signup page and handles user registration.
    Creates a new user, logs them in, and redirects to the homepage.
    If there are validation errors, it provides appropriate error messages.
    '''
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
                                           email=email, bio=description, role=Role.REGISTERED)
                user.save()
                django_user = DjangoUser.objects.create_user(username=username, password=password)
                login(request, django_user)
                return redirect("homepage")

    return render(request, "signup.html", {"message": message})

def logout_page(request):
    '''
    Logs out the current user and redirects to the homepage.
    '''
    logout(request)
    return redirect("homepage")

def forgot_password(request):
    '''
    Renders the forgot password page.
    '''
    return render(request, "zaboravljena_lozinka.html")

def become_judge(request):
    '''
    Renders the become a judge page.
    '''
    return render(request, "postani_ziri.html")\

def search_users(request):
    '''
    Handles user search functionality.
    On POST request, it retrieves the search input and filters users based on username, first name,
    last name, or a combination of first and last name. The filtered results are then displayed
    on the users page along with the original input. Resubmit is called after every pressed key, but
    with debounce period, so that it doesn't lose input.
    '''
    users = User.objects.all()
    input= ""
    filtered = None
    if request.method == "POST":
        input = request.POST.get("search")
        if input != "":
            filtered = list(users.filter(username__icontains=input))
            filtered += list(users.filter(first_name__icontains=input))
            filtered += list(users.filter(last_name__icontains=input))
            split = input.split(" ")
            if split.__len__() > 1:
                first_n = split[0]
                last_n = split[1]
                print(first_n)
                print(last_n)
                filtered += list(users.filter(first_name__icontains=first_n, last_name__icontains=last_n))
            filtered = list(set(filtered))

    return render(request, "korisnici.html", {"users": users, "filtered": filtered, "input": input})


def add_pfp_page(request):
    '''
    Renders the add profile picture page.
    '''
    return render(request, "dodaj_proflnu.html")

def add_pfp(request):
    '''
    Handles the addition of a profile picture for the logged-in user.
    On POST request with an image file, it saves the image to the static directory, updates the user's profile
    picture URL, and renders the profile page with the updated information. 
    If the user already has a profile picture, it deletes the old one before saving the new one.
    '''
    djuser = request.user
    user = User.objects.filter(username=djuser.username).first()
    if request.method == "POST" and request.FILES.get('image') is not None:
        if user.pfp_url is not None:
            delete_picture(user)
        image = request.FILES.get("image")
        if image.content_type.startswith('image/'):
            base, ext = os.path.splitext(image.name)
            filename = f'{djuser.username}{ext}'
            path = os.path.join(settings.BASE_DIR,'static', 'img', filename)

            with open(path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            image_url = f'/static/img/{filename}'
            user.pfp_url = image_url
            user.save()
    return render(request, 'moj_profil.html', {"me":user})


def add_jury_doc(request):
    '''
    Handles the submission of a jury application document for the logged-in user.
    On POST request with a document file, it saves the document to the server, creates a
    Juryrequest entry in the database, and renders the profile page with the updated information.
    '''
    djuser = request.user
    print(djuser.username)
    user = User.objects.filter(username=djuser.username).first()
    if request.method == "POST" and request.FILES.get('cv') is not None:
        cv = request.FILES.get("cv")
        print(cv)
        print(cv.content_type)
        if cv.content_type.startswith('text/') or cv.content_type.startswith('application/'):
            print("starts with cv")
            base, ext = os.path.splitext(cv.name)
            filename = f'{djuser.username}_{base}{ext}'
            print(filename)
            path = os.path.join(settings.BASE_DIR, 'static', 'user_docs', filename)

            with open(path, 'wb+') as destination:
                for chunk in cv.chunks():
                    destination.write(chunk)

            cv_url = f'/static/user_docs/{filename}'
            Juryrequest.objects.create(document_url=cv_url, applicant=user).save()
    return render(request, 'moj_profil.html', {"me": user})


def fund(request, artist_id):
    '''
    Renders the funding page for a specific artist.
    '''
    return render(request, "fundiraj.html", {"artist_id": artist_id})

def pay(request, artist_id):
    '''
    Handles the funding process for a specific artist using PayPal.
    On POST request, it retrieves the donor's email and funding amount, creates a Funding entry
    in the database, obtains a PayPal access token, creates a PayPal order, and redirects the user
    to the PayPal approval URL for payment. If any validation fails, it redirects to the homepage.
    On GET request, it simply renders the funding page.
    '''
    if request.method == "POST":
        email = request.POST.get("email")
        artist = User.objects.filter(id=artist_id).first()
        if artist is None:
            return redirect("homepage")

        donor = User.objects.filter(email=email).first()
        if donor is None:
            return redirect("homepage")

        amount = request.POST.get("amount")
        if amount is None or amount == "":
            return redirect("homepage")

            #commit=False
        funding = Funding.objects.create(amount=amount, donor=donor, artist=artist)
        print("Funding id: " , funding.id)

        #dobijanje tokena
        auth = (PAYPAL_CLIENT_ID, PAYPAL_SECRET)
        token_response = requests.post(
            f"{PAYPAL_API}/v1/oauth2/token",
            data={"grant_type": "client_credentials"},
            auth=auth
        )
        token = token_response.json().get("access_token")

        #pravljenje paypal ordera
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        order_data = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {"currency_code": "EUR", "value": str(amount)},
                "description": f"Fundiranje umetnika {artist.username}"
            }],
            "application_context": {
                "return_url": f"http://127.0.0.1:8000/fund/success/{funding.id}/",
                "cancel_url": f"http://127.0.0.1:8000/fund/cancel/{funding.id}/"
            }
        }
        order_response = requests.post(f"{PAYPAL_API}/v2/checkout/orders", json=order_data, headers=headers)
        order_json = order_response.json()

        approval_url = next((link["href"] for link in order_json["links"] if link["rel"] == "approve"), None)

        funding.payment_id = order_json.get("id")
        #todo kolona paypalov id
        funding.save()

        #preusmerim korisnika na paypal stranicu za placanje:
        return redirect(approval_url)

    return render(request, "fundiraj.html", {"artist_id": artist_id})


def fund_success(request, funding_id):
    '''
    Handles the successful funding process after PayPal payment approval.
    It captures the PayPal order, updates the funding status to "completed", and renders
    the funding page with a success message.
    '''
    funding = Funding.objects.get(id=funding_id)
    funding.status = "completed" #TODO dodati completed kolonu u db
    funding.save()
    return render(request, "fundiraj.html", {
        "artist_id": funding.artist.id,
        "message": "Uspesno ste podržali umetnika! Hvala!"
    })

def fund_cancel(request, funding_id):
    '''
    Handles the cancellation of the funding process.
    It updates the funding status to "cancelled" and renders the funding page with a cancellation message.
    '''
    funding = Funding.objects.get(id=funding_id)
    funding.status = "cancelled"
    funding.save()
    return render(request, "fundiraj.html", {
        "artist_id": funding.artist.id,
        "message": "Plaćanje je otkazano."
    })


def delete_profile(request):
    '''
    Deletes the profile of the logged-in user.
    It removes the user's profile picture if it exists, deletes the user from both
    the custom User model and the Django User model, and redirects to the homepage.
    '''
    username = request.user.username

    user = User.objects.filter(username=username).first()
    if user.pfp_url is not None:
        delete_picture(user)
    user.delete()
    DjangoUser.objects.filter(username=username).first().delete()
    return redirect("homepage")

def edit_profile(request):
    '''
    Renders the edit profile page for the logged-in user.
    It fetches the user's current information and passes it to the template for editing.
    '''
    user = User.objects.get(username = request.user.username)
    return render(request, "izmeni_profil.html", {"me": user})

def save_profile_edits(request):
    '''
    Saves the edits made to the logged-in user's profile.
    On POST request, it retrieves the updated information from the form,
    validates it (e.g., unique username), updates the user's details in the database,
    and redirects to the user's profile page.
    On GET, it simply renders the edit profile page.
    '''
    me = User.objects.filter(username=request.user.username).first()
    if me is None:
        return redirect("homepage")

    if request.method == "POST":
        first_name = request.POST.get("first_name").strip()
        last_name = request.POST.get("last_name").strip()
        username = request.POST.get("username").strip()
        bio = request.POST.get("bio").strip()

        if first_name:
            me.first_name = first_name
        if last_name:
            me.last_name = last_name
        if username and username != me.username:

            if User.objects.filter(username=username).exclude(id=me.id).exists():
                #TODO vratiti poruku o zauzetosti usernamea
                return redirect("edit_profile")
            me.username = username
            request.user.username = username
        if bio:
            me.bio = bio

        me.save()
        request.user.save()
        return redirect("my_page")

    return render(request, "moj_profil.html", {"me":me.id})


def delete_picture(user):
    '''
    Just a helper function to remove the picture from the database.

    Deletes the profile picture of the given user from the server.
    It constructs the file path from the user's profile picture URL and removes the file if it exists.
    '''
    relative_path = user.pfp_url.replace('/static/', '')
    file_path = os.path.join(settings.BASE_DIR, 'static', relative_path)

    if os.path.exists(file_path):
        os.remove(file_path)



def reset_password(request, token):
    '''
    Handles the password reset process using a token.
    On POST request, it retrieves the new password from the form, verifies the token,
    updates the user's password in both the custom User model and the Django User model,
    and redirects to the login page. If the request method is not POST, it renders the
    password reset page with the token.
    '''
    if request.method == 'POST':
        new_password = request.POST.get('password')

        email = TokenStorage.get_token(token)
        print(email)
        user = User.objects.get(email=email)
        print(user.username)
        djuser = DjangoUser.objects.get(username=user.username)
        print(djuser.username)
        djuser.set_password(new_password)
        djuser.save()
        user.password_hash = new_password
        user.save()
        return redirect('login_page')
    return render(request, 'promeni_lozinku.html', {'token': token})



def send_reset_email(request):
    '''
    Handles the process of sending a password reset email to the user.
    On POST request, it retrieves the email from the form, checks if a user with that email exists,
    generates a unique token, saves it, constructs a password reset link, and sends an email
    with the reset link to the user. If the email is not found, it provides an error message.
    It then renders the forgot password page with a success or error message. If the request method
    is not POST, it simply renders the forgot password page.
    '''
    if request.method == "POST":
        email = request.POST.get("email")
        print("Mejlic", email)
        user = User.objects.filter(email=email).first()
        if user:
            token = get_random_string(50)
            TokenStorage.save_token(token, email)
            reset_link = request.build_absolute_uri(reverse('reset_password', args=[token]))

            send_mail(
                subject="Reset your password",
                message=f"Click the link to reset your password: {reset_link}",
                from_email=None,
                recipient_list=[email],
                fail_silently=False,
            )
            return render(request, 'zaboravljena_lozinka.html')
        else:
            return render(request, 'zaboravljena_lozinka.html', {'error': 'Email nije pronađen.'})

    return render(request, 'zaboravljena_lozinka.html')





class TokenStorage:
    '''
    Helper class forgot_password storing tokens used for sendin emails.

    A simple in-memory storage for password reset tokens.
    '''

    token_dict = {}

    @staticmethod
    def save_token(token, email):
        '''
        Saves the token and email in the token dictionary.
        '''
        TokenStorage.token_dict[token] = email

    @staticmethod
    def get_token(token):
        '''
        Returns the email associated with the given token from the token dictionary.
        '''
        return TokenStorage.token_dict.get(token)