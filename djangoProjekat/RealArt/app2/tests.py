from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
from django.contrib.auth.models import User as DjangoUser
from unittest.mock import Mock
from app3.views import addPicture, exhibition
from app1.models import User as AppUser, User, Painting, Exhibition, Participation , Comment, Juryrequest # <-- User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings
import os
import time

class JuryStatus:
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

# Funkcije
def create_user_with_role(role, username="mina"):
    return User.objects.create(
        username=username,
        password_hash="mina123",
        email=f"{username}@test.com",
        role=role
    )

def create_exhibition(user, name="Test Exhibition"):
    return Exhibition.objects.create(
        name=name,
        theme="Test Theme",
        description="Test desc",
        start_date=timezone.now().date() - timedelta(days=1),
        end_date=timezone.now().date() + timedelta(days=1),
        status="active",
        created_by=user,
        winner_painting=None
    )

def create_painting(user, title="Mona Lisa Test", image_url="/static/img/testImage.webp", avg_rating=None):
    return Painting.objects.create(
        title=title,
        image_url=image_url,
        artist=user,
        avg_rating=avg_rating
    )

def create_participation(painting, exhibition):
    return Participation.objects.create(
        painting=painting,
        exhibition=exhibition
    )




"""Test klasa za prikaz jedne izlozbe"""
class ExhibitionPageTest(TestCase):

    """Setupovanje stranice pirkaz jedne izlozbe"""
    def setUp(self):
        self.client = Client()

        self.artist1 = create_user_with_role("registered", "artist1")
        self.artist2 = create_user_with_role("registered", "artist2")

        self.exhibition = create_exhibition(self.artist1, "Jesnja izložba")

        self.painting1 = create_painting(self.artist1, "Sunset", avg_rating=4.5)
        self.painting2 = create_painting(self.artist2, "Morning", avg_rating=3.2)

        create_participation(self.painting1, self.exhibition)
        create_participation(self.painting2, self.exhibition)


    def test_exhibition_page_status_code(self):
        """Provera da li se stranica izložbe učitava"""
        url = reverse('exhibition', args=[self.exhibition.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_exhibition_context(self):
        """Provera da li je izložba prosleđena u context"""
        url = reverse('exhibition', args=[self.exhibition.id])
        response = self.client.get(url)
        izlozba_in_context = response.context['izlozba']
        self.assertEqual(izlozba_in_context.id, self.exhibition.id)
        self.assertEqual(izlozba_in_context.name, self.exhibition.name)

    def test_exhibition_paintings_display(self):
        """Provera da li su slike u context i prikazane u HTML"""
        url = reverse('exhibition', args=[self.exhibition.id])
        response = self.client.get(url)

        paintings_in_context = response.context['paintings']
        painting_titles_in_context = [p.title for p in paintings_in_context]
        self.assertIn(self.painting1.title, painting_titles_in_context)
        self.assertIn(self.painting2.title, painting_titles_in_context)

        self.assertContains(response, self.painting1.title)
        self.assertContains(response, self.painting2.title)





class AddPictureViewTest(TestCase):

    """Setupovanje za dodavanje slike u izlozbu"""
    def setUp(self):
        self.client = Client()
        self.user = create_user_with_role("registered", "artist1")
        self.exhibition = create_exhibition(self.user)
        self.factory = RequestFactory()

        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

    """Provera da ima forma za dodavanje slike"""
    def test_add_picture_get(self):
        url = reverse('addPicture', args=[self.exhibition.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dodaj_sliku.html')


    """Provera da se dodate slike prikazuju na stranici"""
    def test_add_picture_post_creates_painting_and_participation(self):
        url = reverse('addPicture', args=[self.exhibition.id])
        test_image = SimpleUploadedFile("test.jpg", b'test image content', content_type="image/jpeg")

        request = self.factory.post(url, {
            'title': 'Nova Slika',
            'description': 'Opis slike',
            'image': test_image
        })

        request.user = Mock(is_authenticated=True, username=self.user.username)
        request.session = self.client.session

        response = addPicture(request, self.exhibition.id)

        painting = Painting.objects.get(title='Nova Slika')
        self.assertEqual(painting.artist, self.user)
        self.assertTrue(Participation.objects.filter(painting=painting, exhibition=self.exhibition).exists())

        import os
        from django.conf import settings

        if painting.image_url:
            relative_path = painting.image_url.replace('/static/', '')
            file_path = os.path.join(settings.BASE_DIR, 'static', relative_path)
            if os.path.exists(file_path):
                os.remove(file_path)

    """Provera da li guest vidi dugme za dodavanje slike u izlozbu"""
    def test_guest_user_does_not_see_add_picture_button(self):
        url = reverse('exhibition', args=[self.exhibition.id])
        response = self.client.get(url)


        self.assertNotContains(response, "Dodaj sliku")




class AdminUsViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin = create_user_with_role("admin", "admin")
        # ručno logovanje admina
        session = self.client.session
        session['user_id'] = self.admin.id
        session.save()

        self.artist = create_user_with_role("registered", "artist1")

    """Kreiranje slike sa komentarima"""
    def create_painting_with_comment(self):
        painting = create_painting(self.artist, "Test Painting")
        comment = Comment.objects.create(
            painting=painting,
            author=self.artist,
            text="Test komentar"
        )
        return painting, comment

    """Zahtev za zirija"""
    def create_jury_request(self):
        return Juryrequest.objects.create(
            applicant=self.artist,
            status=JuryStatus.PENDING
        )

    """Test admin prihvata zahteve za ziri"""
    def test_admin_accept_jury_request(self):
        jury_request = self.create_jury_request()
        url = reverse('adminUs')
        response = self.client.post(url, {'akcija': 'prihvati', 'request_id': jury_request.id}, follow=True)
        jury_request.refresh_from_db()
        self.assertEqual(jury_request.status, JuryStatus.APPROVED)

    """Test admin odbija zahteve za ziri"""
    def test_admin_reject_jury_request(self):
        jury_request = self.create_jury_request()
        url = reverse('adminUs')
        response = self.client.post(url, {'akcija': 'odbij', 'request_id': jury_request.id}, follow=True)
        jury_request.refresh_from_db()
        self.assertEqual(jury_request.status, JuryStatus.REJECTED)

    """Provera brisanja slike od strane admina"""
    def test_admin_delete_painting(self):
        painting, comment = self.create_painting_with_comment()
        Comment.objects.filter(painting=painting).delete()

        url = reverse('adminUs')
        response = self.client.post(url, {'akcija': 'brisanje', 'painting_id': painting.id}, follow=True)
        self.assertFalse(Painting.objects.filter(id=painting.id).exists())

    """Test brisanja komentara od strane admina"""
    def test_admin_delete_comment(self):
        painting, comment = self.create_painting_with_comment()
        url = reverse('adminUs')
        response = self.client.post(url, {'akcija': 'brisanje_komentara', 'comment_id': comment.id}, follow=True)
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())


class GalleryViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="artist1", password_hash="123", email="a@test.com", role="registered")


        self.exhibition = Exhibition.objects.create(
            name="Test Exhibition",
            theme="Tema 1",
            description="Opis izložbe",
            start_date="2025-01-01",
            end_date="2025-12-31",
            status="active",
            created_by=self.user
        )


        self.painting1 = Painting.objects.create(
            title="Slika 1",
            image_url="/static/img/test1.webp",
            artist=self.user
        )
        self.painting2 = Painting.objects.create(
            title="Slika 2",
            image_url="/static/img/test2.webp",
            artist=self.user
        )


        Participation.objects.create(painting=self.painting1, exhibition=self.exhibition)
        Participation.objects.create(painting=self.painting2, exhibition=self.exhibition)

    """Test status galerije - radova"""
    def test_gallery_view_status_and_template(self):
        url = reverse('gallery')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'galerija.html')

    """Galerija sa prikazom slika"""
    def test_gallery_context_contains_paintings(self):
        url = reverse('gallery')
        response = self.client.get(url)
        paintings_context = response.context['paintings']

        painting_titles = [item['painting'].title for item in paintings_context]
        self.assertIn(self.painting1.title, painting_titles)
        self.assertIn(self.painting2.title, painting_titles)

        themes_list = [theme for item in paintings_context for theme in item['themes']]
        self.assertIn(self.exhibition.theme, themes_list)


class ChooseWinnerButtonTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.jury_user = create_user_with_role("jury", "jury_creator")

        session = self.client.session
        session['user_id'] = self.jury_user.id
        session.save()

        self.exhibition = create_exhibition(self.jury_user, "Moja izložba")
        self.exhibition.status = "closed"  # završena
        self.exhibition.save()

    def test_user_is_jury_and_creator(self):
        """Testiramo da li je user jury i kreator izložbe"""
        self.assertEqual(self.jury_user.role, "jury", "User nije jury!")
        self.assertEqual(self.exhibition.created_by, self.jury_user, "User nije kreator izložbe!")



class WebdriverUITest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # relativna putanja do geckodriver-a u app2/webdrivers folderu
        gecko_path = os.path.join(settings.BASE_DIR, 'app2', 'webdriver', 'geckodriver.exe')

        options = Options()
        service = Service(executable_path=gecko_path)

        cls.browser = webdriver.Firefox(service=service, options=options)
        cls.browser.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        self.app_user = AppUser.objects.create(
            username="mina",
            password_hash="Test12345",
            email="mina@test.com",
            role="registered"
        )

        self.django_user = DjangoUser.objects.create_user(
            username="mina",
            password="Test12345"
        )


        self.exhibition = Exhibition.objects.create(
            name="Test Exhibition",
            theme="Tema 1",
            description="Opis izložbe",
            start_date=timezone.now().date() - timedelta(days=1),
            end_date=timezone.now().date() + timedelta(days=1),
            status="active",
            created_by=self.app_user
        )
        self.painting = Painting.objects.create(
            title="Slika1",
            image_url="/static/img/slobodna1.jpg",
            artist=self.app_user
        )
        Participation.objects.create(
            painting=self.painting,
            exhibition=self.exhibition
        )


    """Test da li je dugme dodaj sliku vidiljivo za ulogovanog korisnika"""
    def test_add_picture_button_visible_for_logged_in_user(self):
        # 1. Poseta login stranici
        self.browser.get(f"{self.live_server_url}/login/")
        self.browser.find_element(By.NAME, "username").send_keys("mina")
        self.browser.find_element(By.NAME, "password").send_keys("Test12345")
        self.browser.find_element(By.XPATH, "//button[@type='submit']").click()

        WebDriverWait(self.browser, 5).until(
            lambda driver: driver.current_url != f"{self.live_server_url}/login/"
        )

        self.browser.get(f"{self.live_server_url}/exhibition/{self.exhibition.id}/")

        try:
            button = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Dodaj sliku')]"))
            )
            self.assertTrue(button.is_displayed(), "Dugme Dodaj sliku nije vidljivo za ulogovanog korisnika")
        except Exception as e:
            self.fail(f"Dugme Dodaj sliku nije pronađeno: {e}")

    def test_add_picture_button_not_visible_for_guest(self):
        """Provera da li guest NE vidi dugme 'Dodaj sliku'"""
        self.browser.get(f"{self.live_server_url}/exhibition/{self.exhibition.id}/")
        buttons = self.browser.find_elements(By.XPATH, "//button[contains(text(),'Dodaj sliku')]")
        self.assertEqual(len(buttons), 0, "Dugme Dodaj sliku je vidljivo za neulogovanog korisnika")

    def test_exhibition_page_displays_correctly(self):
        """Provera da li se izložba pravilno prikazuje na stranici"""

        self.browser.get(f"{self.live_server_url}/exhibition/{self.exhibition.id}/")

        body_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertIn(self.exhibition.name, body_text, "Naziv izložbe nije prikazan na stranici")

        try:
            image_element = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, f"//img[contains(@src, '{self.painting.image_url}')]"))
            )
            self.assertTrue(image_element.is_displayed(), "Slika iz izložbe nije prikazana")
        except:
            self.fail("Slika iz izložbe nije pronađena na stranici")

