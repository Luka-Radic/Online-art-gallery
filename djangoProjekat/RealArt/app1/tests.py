from datetime import date, timedelta
import time
from telnetlib import EC

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
import logging

from selenium.webdriver.support.wait import WebDriverWait

logging.basicConfig(level=logging.DEBUG)

from django.contrib.auth.models import User as DjangoUser

from app1.models import User as AppUser, Painting, Exhibition
# from app2.models import Painting, Exhibition



class WebdriverUITest(StaticLiveServerTestCase):

    def setUp(self):

        self.service = EdgeService(
            executable_path=r"C:\Users\Mina\Desktop\PSIgerrit\project_RealArt\djangoProjekat\RealArt\app1\edgedriver_win64\msedgedriver.exe")
        self.browser = webdriver.Edge(service=self.service)
        self.browser.implicitly_wait(5)
        self.app_url = self.live_server_url + "/exhibitions/"

        # Kreiramo test korisnika (koji će moći da se prijavi)
        self.app_user = AppUser.objects.create(username="mina", password_hash="Test12345", email="m@gmail")
        self.django_user = DjangoUser.objects.create_user(username="mina", password="Test12345")


        # Kreiramo test sliku i izložbu da imamo podatke za prikaz
        self.painting = Painting.objects.create(
            title="Test Slika",
            image_url="/static/img/mona_lisa.webp",
            artist=self.app_user,
            image_desc="Test opis slike"
        )

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
