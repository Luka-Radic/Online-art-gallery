from django.db import transaction, IntegrityError
from django.test import TestCase
import unittest
import time
from datetime import date, timedelta
from django.test import TestCase, Client, SimpleTestCase
from django.urls import resolve, reverse
from django.utils import timezone
from django.contrib.auth.models import User as DjangoUser
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.views.generic import detail

from app1.models import User as AppUser, Exhibition, Participation
from app1.views import *
from selenium import webdriver
from selenium.webdriver.common.by import By

def create_exhibition(user, name):
    exhibition = Exhibition.objects.create(
        name=name,
        theme="Test Theme",
        description="Test desc",
        start_date=timezone.now().date() - timedelta(days=1),
        end_date=timezone.now().date() + timedelta(days=1),
        status="closed",
        created_by=user,
        winner_painting=None
    )
    return exhibition


def create_painting(user):
    painting = Painting.objects.create(
        title="Mona Lisa Test",
        image_url="/static/img/testImage.webp",
        artist=user
    )
    return painting


def create_participation(painting, exhibition):
    Participation.objects.create(
        painting=painting,
        exhibition=exhibition
    )


def create_user_with_role(role, par=0):
    username = ""
    password_hash = ""
    email = ""
    cnt = str(par)
    if role == "guest":
        first_name = "ime"
        last_name = "prezime"
        username = "noviGuest" + cnt
        password_hash = "passwordGuest12"
        email = cnt + "noviguest@test.com"
        bio = "bio"
    elif role == "registered":
        first_name = "ime"
        last_name = "prezime"
        username = "noviRegistered" + cnt
        password_hash = "passwordRegistered12" + cnt
        email = cnt + "noviRegistered@test.com"
        bio = "bio"
    elif role == "jury":
        first_name = "ime"
        last_name = "prezime"
        username = "noviJury" + cnt
        password_hash = "passwordJury12" + cnt
        email =cnt + "noviJury@test.com"
        bio = "bio"
    else:
        first_name = "ime"
        last_name = "prezime"
        username = "noviAdmin" + cnt
        password_hash = cnt + "passwordAdmin12"
        email = cnt + "noviAdmin@test.com"
        bio = "bio"
    user = AppUser.objects.create(username=username, password_hash=password_hash,email=email,role=role, first_name=first_name, last_name=last_name, bio = "bio")
    return user


def new_exhibition_data(jury):
    return {
        "name": "new exhibition",
        "theme": "theme",
        "description": "desc",
        "start_date": timezone.now().date(),
        "end_date": timezone.now().date() + timedelta(days=2),
        "created_by": jury
    }


class UnitTestsGuest(TestCase):

    def setUp(self):
        self.user_guest = create_user_with_role("guest")
        self.user_artist = create_user_with_role("registered")
        self.django_user_guest = DjangoUser.objects.create(username=self.user_guest.username, password=self.user_guest.password_hash)
        self.django_user_artist = DjangoUser.objects.create(username=self.user_artist.username, password=self.user_artist.password_hash)
        self.client.login(username=self.user_guest.username, password=self.user_guest.password_hash)

    def test_homepage_get(self):
        """Ovaj test proverava da li se guest-u normalno ucitava pocetna stranica"""
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_users_get(self):
        """Ovaj test proverava da li se guest-u normalno ucitava users stranica"""
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user_guest.username)

    def test_my_page_get(self):
        """Ovaj test proverava da li se guest-u ne prikazuje Moj Profil sekcija"""
        try:
            self.client.get(reverse('my_page'))
        except AttributeError as e:
            self.assertIn("'NoneType' object has no attribute 'id'", str(e))
        else:
            self.fail("AttributeError nije podignut kako se očekuje")

    def test_artist_page(self):
        """Ovaj test proverava da li se guest-u prikazuje artist page"""
        response = self.client.get(reverse('artist', args=[self.user_artist.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user_artist.username)

    def test_login_page(self):
        """Ovaj test proverava login stranicu"""
        response = self.client.get(reverse('login_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Korisničko ime")
        self.assertContains(response, "Lozinka")
        self.assertContains(response, "Prijavi se")

    def test_signup_page(self):
        """Ovaj test proverava signup stranicu"""
        response = self.client.get(reverse('signup_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ime")
        self.assertContains(response, "Prezime")
        self.assertContains(response, "Korisničko ime")
        self.assertContains(response, "Lozinka")
        self.assertContains(response, "Potvrda lozinke")
        self.assertContains(response, "Email adresa")
        self.assertContains(response, "Opis")
        self.assertContains(response, "Prijavi se")

    def test_successful_signup(self):
        """Ovaj test proverava da li sign up zaista radi za ispravne unete podatke"""
        response = self.client.post(reverse('signup_page'), {
            "ime": "Ana",
            "prezime": "Anić",
            "korisnickoIme": "anica123",
            "lozinka": "tajna123",
            "potvrdaLozinke": "tajna123",
            "email": "ana@example.com",
            "opis": "Volim umetnost"
        })
        self.assertEqual(response.status_code, 302)

    def test_signup_duplicate_username(self):
        """Ovaj test proverava da li je uneto username koje vec postoji"""
        AppUser.objects.create(
            username="anica123",
            password_hash="tajna123",
            email="ana@example.com",
            role="registered"
        )

        response = self.client.post(reverse('signup_page'), {
            "ime": "Ana",
            "prezime": "Anić",
            "korisnickoIme": "anica123",  # već postoji
            "lozinka": "tajna123",
            "potvrdaLozinke": "tajna123",
            "email": "nova@example.com"
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Korisnik sa tim korisnickim imenom vec postoji. Unesite drugo.")

    def test_signup_duplicate_email(self):
        """Ovaj test proverava da li unet email vec postoji"""
        AppUser.objects.create(
            username="originalUser",
            password_hash="tajna123",
            email="ana@example.com",
            role="registered"
        )

        response = self.client.post(reverse('signup_page'), {
            "ime": "Ana",
            "prezime": "Anić",
            "korisnickoIme": "anica123",
            "lozinka": "tajna123",
            "potvrdaLozinke": "tajna123",
            "email": "ana@example.com"  # već postoji
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Korisnik sa tim email-om vec postoji.")

    def test_signup_missing_ime(self):
        """Ovaj test proverava da li signup ne radi ako nije uneto ime"""
        self.client.post(reverse('signup_page'), {
            "prezime": "Anić",
            "korisnickoIme": "anica123",
            "lozinka": "tajna123",
            "potvrdaLozinke": "tajna123",
            "email": "ana@example.com"
        })
        user = AppUser.objects.get(username="anica123")
        self.assertIsNone(user.first_name)

    def test_signup_missing_prezime(self):
        """Ovaj test proverava da li sign up ne radi ako prezime nije uneto"""
        self.client.post(reverse('signup_page'), {
            "prezime": "Anić",
            "korisnickoIme": "anica123",
            "lozinka": "tajna123",
            "potvrdaLozinke": "tajna123",
            "email": "ana@example.com"
        })
        user = AppUser.objects.get(username="anica123")
        self.assertIsNone(user.first_name)

    def test_signup_missing_username(self):
        """Ovaj test proverava da li signup baca IntegrityError ako nije unet username"""
        try:
            self.client.post(reverse('signup_page'), {
                "ime": "Ana",
                "prezime": "Anić",
                "lozinka": "tajna123",
                "potvrdaLozinke": "tajna123",
                "email": "ana@example.com"
            })
        except IntegrityError:
            pass
        else:
            self.fail("IntegrityError nije podignut za nedostajući username")

    def test_signup_missing_password(self):
        """Ovaj test proverava da li signup ne radi ako nije unet password"""
        self.client.post(reverse('signup_page'), {
            "ime": "Ana",
            "prezime": "Anić",
            "korisnickoIme": "anica123",
            "potvrdaLozinke": "tajna123",
            "email": "ana@example.com"
        })
        self.assertFalse(AppUser.objects.filter(username="anica123").exists())

    def test_signup_missing_password_confirmation(self):
        """Ovaj test proverava da li se signup nije izvrsio ako guest nije uneo potvrdu lozinke"""
        self.client.post(reverse('signup_page'), {
            "prezime": "Anić",
            "korisnickoIme": "anica123",
            "lozinka": "tajna123",
            "potvrdaLozinke": "tajna123",
            "email": "ana@example.com"
        })
        user = AppUser.objects.get(username="anica123")
        self.assertIsNone(user.first_name)

    def test_signup_missing_email(self):
        """Ovaj test provera da li se signup nije izvrsio ako guest nije uneo email polje"""
        try:
            self.client.post(reverse('signup_page'), {
                "ime": "Ana",
                "prezime": "Anić",
                "korisnickoIme": "anica123",
                "lozinka": "tajna123",
                "potvrdaLozinke": "tajna123"
            })
        except IntegrityError:
            pass
        else:
            self.fail("IntegrityError nije podignut za nedostajući email")

    def test_logout_get(self):
        """Ovaj test proverava da li je login nemoguc za guesta"""
        response = self.client.get(reverse('homepage'))
        self.assertNotContains(response, "Log out")

class UnitTestRegistered(TestCase):

    def setUp(self):
        self.user_artist = create_user_with_role("registered",1)
        self.user_artist_2 = create_user_with_role("registered",2)
        self.django_user_artist = DjangoUser.objects.create_user(username=self.user_artist.username, password=self.user_artist.password_hash)
        self.django_user_artist_2 = DjangoUser.objects.create_user(username=self.user_artist_2.username, password=self.user_artist_2.password_hash)
        self.client.login(username=self.user_artist.username, password=self.user_artist.password_hash)
        self.funding = Funding.objects.create(donor=self.user_artist, artist=self.user_artist_2, amount=100.23)

    def test_homepage_get(self):
        """Ovaj test proverava da li se registered-u normalno ucitava pocetna stranica"""
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_users_get(self):
        """Ovaj test proverava da li se registered-u normalno ucitava users stranica"""
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user_artist.username)

    def test_my_page_get(self):
        """Ovaj test proverava da li se registered-u prikazuje Moj Profil sekcija"""
        response = self.client.get(reverse('my_page'))
        self.assertContains(response, self.django_user_artist.username)
        self.assertContains(response, "Pregled radova")
        self.assertContains(response, "Nazad")
        self.assertContains(response, "Umetnik")

    def test_artist_page(self):
        """Ovaj test proverava da li se registered-u prikazuje artist page"""
        response = self.client.get(reverse('artist', args=[self.user_artist.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user_artist.username)

    def test_login_page(self):
        """Ovaj test proverava login stranicu za registered-a"""
        self.client.logout()
        response = self.client.get(reverse('login_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Korisničko ime")
        self.assertContains(response, "Lozinka")
        self.assertContains(response, "Prijavi se")

    def test_login_successful(self):
        """Ovaj test proverava uspesan login za registered korisnika"""
        status = self.client.login(username=self.user_artist.username, password=self.user_artist.password_hash)
        self.assertTrue(status)

    def test_login_unsuccessful(self):
        """Ovaj test proverava logout za registered korisnika sa unetim losim podacima"""
        self.client.logout()
        status = self.client.login(username=self.user_artist.username, password="12345vvv")
        self.assertFalse(status)

    def test_logout_get(self):
        """Ovaj test proverava da li login radi za registered korisnika"""
        response = self.client.get(reverse('logout_page'))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_forgot_password(self):
        """Ovaj test testira da li forgot password stranica radi"""
        response = self.client.get(reverse('forgot_password'))
        self.assertEqual(response.status_code, 200)

    def test_become_judge(self):
        """Ovaj test testira da li zahtev za zirija od registered korisniika radi"""
        response = self.client.get(reverse('become_judge'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dostavite vašu dokumentaciju sa kvalifikacijom (CV)")

    def test_search_users(self):
        """Ovaj test testira pretragu korisnika za registered korisnika"""
        response = self.client.get(reverse('search_users'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.django_user_artist.username)

    def test_add_pfp_page(self):
        """Ovaj test testira stranicu za dodavanje pfp slike za registered korisnika"""
        response = self.client.get(reverse('add_pfp_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dodaj sliku")

    def test_add_pfp(self):
        """Ovaj test testira prihvatanje slike i postavljanje za profilnu"""
        response = self.client.get(reverse('add_pfp'))
        self.assertEqual(response.status_code, 302)

    def test_add_jury_doc(self):
        """Ovaj test testira dodavanje dokumenata za sudiju"""
        response = self.client.get(reverse('add_jury_doc'))
        self.assertEqual(response.status_code, 200)

    def test_fund(self):
        """Ovaj test testira fund funkcionalnost za registered korisnika"""
        response = self.client.get(reverse('fund', args=[self.django_user_artist_2.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Podrži umetnika")
        self.assertContains(response, "Izaberi iznos")

    def test_fund_success(self):
        """Ovaj test testira uspesno fundiranje registered korisnika"""
        response = self.client.get(reverse('fund_success', args=[self.funding.id]))

    def test_fund_cancel(self):
        """Ovaj test testira fund cancel opciju za registred korisnika"""
        response = self.client.get(reverse('fund_cancel', args=[self.funding.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Plaćanje je otkazano.")

    def test_delete_profile(self):
        """Ovaj test proverava brisanje profila"""
        response = self.client.get(reverse('delete_profile'))
        self.assertEqual(response.status_code, 302)
        user = User.objects.filter(username=self.user_artist.username).first()
        self.assertEqual(user, None)

    def test_edit_profile(self):
        """Ovaj test testira izmenu stvari na profilu"""
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dodaj profilnu sliku")
        self.assertContains(response, "Obrisi moj profil")

    def test_save_profile_edit(self):
        """Ovaj test testira cuvanje izmena profila"""
        self.client.login(username=self.user_artist_2.username, password=self.user_artist_2.password_hash)
        old_username = self.user_artist_2.username
        response = self.client.post(reverse('save_profile_edits'), data={
            'username': self.user_artist_2.username + "novoooo",
            'email': 'novii' + self.user_artist_2.email,
            'first_name': 'noviii' + self.user_artist_2.first_name,
            'last_name': 'noviii' + self.user_artist_2.last_name,
            'bio': self.user_artist_2.bio,
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.filter(id=self.user_artist_2.id).first()
        self.assertNotEqual(old_username, user.username)

