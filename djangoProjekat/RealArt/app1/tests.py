import os.path
import unittest
from datetime import date, timedelta
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
import logging
logging.basicConfig(level=logging.DEBUG)

from RealArt import settings

from django.contrib.auth.models import User as DjangoUser
from app1.models import User as AppUser, Painting, Exhibition, Participation, Comment, Rating



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

def create_user_with_role(role):
    user = AppUser.objects.create(
        username="mina",
        password_hash="mina123",
        email="mina@test.com",
        role=role
    )
    return user

def new_exhibition_data(jury):
    return {
        "name": "new exhibition",
        "theme": "theme",
        "description": "desc",
        "start_date": timezone.now().date(),
        "end_date": timezone.now().date() + timedelta(days=2),
        "created_by":jury
    }



class UnitTestsRegistered(TestCase):

    def setUp(self):
        self.user = create_user_with_role("registered")
        self.django_user = DjangoUser.objects.create_user(username=self.user.username, password=self.user.password_hash)

        self.client.login(username=self.user.username, password=self.user.password_hash)

        self.painting = create_painting(self.user)
        self.exhibition = create_exhibition(self.user, "Test Exhibition")
        create_participation(self.painting, self.exhibition)


    def tearDown(self):
        self.client.get(reverse('logout_page'))


    def test_exhibitions_get(self):
        ''' proverava da li se otvara stranica i da li je dodata izlozba od gore '''
        print("\nexhibition page rendering properly: ")
        response = self.client.get(reverse('exhibitions'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('izlozbe_sa_slikom', response.context)
        self.assertEqual(len(response.context['izlozbe_sa_slikom']), 1)
        self.assertEqual(response.context['izlozbe_sa_slikom'][0]['slika'], self.painting.image_url)


    def test_image_detail_get(self):
        """Proverava GET /image_<id>/ vraca sliku, komentare i ocene"""
        print("\nimage detail rendering properly: ")
        response = self.client.get(reverse('image_detail', args=[self.painting.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['painting'].title, self.painting.title)
        self.assertEqual(response.context['avg_rating'], 0)
        self.assertEqual(response.context['user_rating'], None)


    def test_image_detail_post_comment(self):
        """Dodavanje komentara"""
        print("\ncomment creating: ")
        response = self.client.post(reverse('image_detail', args=[self.painting.id]), {
            'comment_text': 'Great painting!'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        comment = Comment.objects.filter(painting=self.painting, author=self.user).first()
        self.assertIsNotNone(comment)
        self.assertEqual(comment.text, 'Great painting!')


    def test_image_detail_post_rating_create(self):
        """Dodavanje nove ocene"""
        print("\nstar creating test: ")
        response = self.client.post(reverse('image_detail', args=[self.painting.id]), {
            'rating_value': '5'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        rating = Rating.objects.filter(painting=self.painting, author=self.user).first()
        self.assertIsNotNone(rating)
        self.assertEqual(rating.score, 5)

    def test_image_detail_post_rating_update_and_delete(self):
        """Menjanje ocene ili brisanje klikom na istu ocenu"""
        print("\nstar update/delete test: ")
        Rating.objects.create(painting=self.painting, author=self.user, score=3)

        response = self.client.post(reverse('image_detail', args=[self.painting.id]), {
            'rating_value': '4'
        })
        rating = Rating.objects.filter(painting=self.painting, author=self.user).first()
        self.assertEqual(rating.score, 4)

        response = self.client.post(reverse('image_detail', args=[self.painting.id]), {
            'rating_value': '4'
        })
        self.assertFalse(Rating.objects.filter(painting=self.painting, author=self.user).exists())


    def test_exhibition_form_not_visible_for_registered(self):
        ''' Proverava da li role=registered user vidi uopste kreiranje izlozbe '''
        print("\n\nREGULAR TESTS:")
        print("\nregular user doesn't see create exhibition form: ")
        response = self.client.get(reverse('exhibitions'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '+ Napravi novu izložbu')




class UnitTestsJury(TestCase):

    def setUp(self):
        self.user = create_user_with_role("jury")
        self.django_user = DjangoUser.objects.create_user(username=self.user.username, password=self.user.password_hash)

        self.client.login(username=self.user.username, password=self.user.password_hash)

        self.painting = create_painting(self.user)
        self.exhibition = create_exhibition(self.user, "Test Exhibition")
        create_participation(self.painting, self.exhibition)


    def tearDown(self):
        self.client.get(reverse('logout_page'))

    def test_exhibitions_post_creates_exhibition(self):
        """Proverava POST kreira novu izložbu"""
        print("\n\nJURY TESTS:")
        print("\ncreating exhibition: ")
        response = self.client.post(reverse('exhibitions'), new_exhibition_data(self.user))
        self.assertEqual(response.status_code, 302)  # redirect
        self.assertTrue(Exhibition.objects.filter(name="new exhibition").exists())

    def test_exhibition_form_visible_for_jury(self):
        ''' Proverava da li role=jury user vidi kreiranje izlozbe '''
        print("\njury user sees create exhibition form: ")
        self.client.force_login(self.django_user)
        response = self.client.get(reverse('exhibitions'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '+ Napravi novu izložbu')  # vidi formu


    def test_jury_create_exhibition_no_theme(self):
        ''' Provera da ne moze izlozba bez teme da se napravi'''
        print("\ncreating exhibition with no theme failing: ")

        data = new_exhibition_data(self.user)
        data['theme'] = ''
        response = self.client.post(reverse('exhibitions'), data)
        self.assertNotEqual(response.status_code, 302)


    def test_jury_create_exhibition_no_name(self):
        ''' Provera da ne moze izlozba bez imena da se napravi'''
        print("\ncreating exhibition with no name failing: ")

        data = new_exhibition_data(self.user)
        data['name'] = ''
        response = self.client.post(reverse('exhibitions'), data)
        self.assertNotEqual(response.status_code, 302)


    # def test_jury_create_exhibition_no_date_from(self):
    #     ''' Provera da ne moze izlozba bez pocetnog datuma da se napravi'''
    #     print("\ncreating exhibition with no date_from failing: ")
    #
    #     data = new_exhibition_data(self.user)
    #     data['date_from'] = ''
    #     response = self.client.post(reverse('exhibitions'), data)
    #     self.assertNotEqual(response.status_code, 302)
    #
    #
    # def test_jury_create_exhibition_no_date_to(self):
    #     ''' Provera da ne moze izlozba bez krajnjeg datuma da se napravi'''
    #     print("\ncreating exhibition with no date_to failing: ")
    #
    #     data = new_exhibition_data(self.user)
    #     data['date_to'] = ''
    #     response = self.client.post(reverse('exhibitions'), data)
    #     self.assertNotEqual(response.status_code, 302)






class UnitTestsGuest(TestCase):

    def setUp(self):
        self.user = create_user_with_role("guest")
        self.django_user = DjangoUser.objects.create_user(username=self.user.username, password=self.user.password_hash)

        self.painting = create_painting(self.user)
        self.exhibition = create_exhibition(self.user, "Test Exhibition")
        create_participation(self.painting, self.exhibition)


    def test_exhibitions_get(self):
        ''' proverava da li se otvara stranica i da li je dodata izlozba od gore '''
        print("\nexhibition page rendering properly for guest: ")
        response = self.client.get(reverse('exhibitions'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('izlozbe_sa_slikom', response.context)
        self.assertEqual(len(response.context['izlozbe_sa_slikom']), 1)
        self.assertEqual(response.context['izlozbe_sa_slikom'][0]['slika'], self.painting.image_url)


    def test_image_detail_get(self):
        """Proverava GET /image_<id>/ vraca sliku, komentare i ocene"""
        print("\nimage detail rendering properly for guest: ")
        response = self.client.get(reverse('image_detail', args=[self.painting.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['painting'].title, self.painting.title)
        self.assertEqual(response.context['avg_rating'], 0)
        self.assertEqual(response.context['user_rating'], None)


    def test_image_detail_post_comment(self):
        """Dodavanje komentara"""
        print("\ncomment creating failing test: ")
        response = self.client.post(reverse('image_detail', args=[self.painting.id]), {
            'comment_text': 'Great painting!'
        }, follow=True)
        comment = Comment.objects.filter(painting=self.painting, author=self.user).first()
        self.assertIsNone(comment)


    def test_image_detail_post_rating_create(self):
        """Dodavanje nove ocene"""
        print("\nstar creating failing test: ")
        response = self.client.post(reverse('image_detail', args=[self.painting.id]), {
            'rating_value': '5'
        }, follow=True)
        rating = Rating.objects.filter(painting=self.painting, author=self.user).first()
        self.assertIsNone(rating)


    def test_exhibition_form_not_visible_for_registered(self):
        ''' Proverava da li role=registered user vidi uopste kreiranje izlozbe '''
        print("\n\nGUEST TESTS:")
        print("\nguest user doesn't see create exhibition form: ")
        response = self.client.get(reverse('exhibitions'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '+ Napravi novu izložbu')





class WebdriverUITest(StaticLiveServerTestCase):

    def setUp(self):
        #  r"C:\Users\Mina\Desktop\PSIgerrit\project_RealArt\djangoProjekat\RealArt\app1\edgedriver_win64\msedgedriver.exe"
        self.service = EdgeService(
            executable_path=os.path.join(settings.BASE_DIR, 'app1\edgedriver_win64\msedgedriver.exe') )
        self.browser = webdriver.Edge(service=self.service)
        self.browser.implicitly_wait(5)
        self.app_url = self.live_server_url + "/exhibitions/"

        # test korisnik
        self.app_user = AppUser.objects.create(username="mina", password_hash="Test12345", email="m@gmail")
        self.django_user = DjangoUser.objects.create_user(username="mina", password="Test12345")


        # test slika
        # create_painting(self.app_user)
        self.painting = Painting.objects.create(
            title="Test Slika",
            image_url="/static/img/mona_lisa.webp",
            artist=self.app_user,
            image_desc="Test opis slike"
        )

        # test izlozba
        # create_exhibition(self.app_user,"Jesnja izložba")
        self.exhibition = Exhibition.objects.create(
            name="Jesnja izložba",
            theme="Umetnost jeseni",
            start_date=date.today() - timedelta(days=1),
            end_date=date.today() + timedelta(days=5),
            created_by=self.app_user,
            status="active"
        )

    def tearDown(self):
        self.browser.quit()


    def login(self):
        """Login fejk usera"""
        self.browser.get(self.live_server_url + "/login/")
        time.sleep(1)
        self.browser.find_element(By.NAME, "username").send_keys("mina")
        self.browser.find_element(By.NAME, "password").send_keys("Test12345")
        self.browser.find_element(By.XPATH, "//button[text()='Prijavi se']").click()
        time.sleep(2)


    def test_login_and_exhibition_navigation(self):
        """Test: prijava i pregled stranice izložbi"""
        self.login()

        self.browser.get(self.live_server_url+"/exhibitions/")
        time.sleep(2)

        naslov = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("Pregled izložbi", naslov)

        kartice = self.browser.find_elements(By.CLASS_NAME, "card-title")
        print ("KARTICEE", kartice)
        for k in kartice:
            print(k.text)
        self.assertTrue(any("Jesnja izložba" in k.text for k in kartice))



    def test_image_detail_comment(self):
        """Test: otvaranje stranice slike i dodavanje komentara"""
        self.login()

        self.browser.get(self.live_server_url+f"/image_{self.painting.id}/")
        time.sleep(5)


        comment_input = self.browser.find_element(By.NAME, "comment_text")
        comment_input.send_keys("Prelepa slika!")
        comment_input.send_keys(Keys.RETURN)
        time.sleep(3)


        comments = self.browser.find_elements(By.CLASS_NAME, "comment-text")
        self.assertTrue(any("Prelepa slika" in c.text for c in comments))
