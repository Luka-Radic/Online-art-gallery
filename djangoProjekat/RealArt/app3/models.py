from datetime import datetime, date
from django.db.models import Avg
from django.contrib.auth.models import User as DjangoUser
from django.db import models
from django.utils import timezone

# helper functions to link Django User and User model
def get_pfp(DjangoUser):
    users = User.objects.filter(username=DjangoUser.username)
    if users.count() != 0 and users.first().pfp_url is not None:
        return users.first().pfp_url
    else:
        return "/static/img/default_pfp.png"
DjangoUser.get_pfp = get_pfp

def get_base_user(DjangoUser):
    users = User.objects.filter(username=DjangoUser.username)
    if users.count() != 0 and users.first().pfp_url is not None:
        return users.first()
    else:
        return None
DjangoUser.get_base_user = get_base_user

#used as Enum in code
class Status(models.TextChoices):
    PENDING = ('pending', 'Prihvaćen')
    APPROVED = ('approved', 'Odobren')
    REJECTED = ('rejected', 'Odbijen')

class Role(models.TextChoices):
    GUEST = ('guest','Gost')
    REGISTERED = ('registered', 'Registrovan')
    JURY = ('jury','Ziri')
    ADMIN = ('admin', 'Administrator')

class Comment(models.Model):
    """
    Model for Comment table.
    """
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    author = models.ForeignKey('app3.User', on_delete=models.CASCADE)
    painting = models.ForeignKey('Painting', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'comment'

class Exhibition(models.Model):
    """
    Model for Exhibition table.
    """
    name = models.CharField(max_length=100)
    theme = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=6)
    created_by = models.ForeignKey('User', models.DO_NOTHING, db_column='created_by')
    winner_painting = models.ForeignKey('Painting', on_delete=models.SET_NULL, blank=True, null=True)

    def is_active(self):
        return self.start_date >= datetime.date.today() >= self.end_date

    def is_finished(self):
        return self.end_date and self.end_date < date.today()

    class Meta:
        managed = False
        db_table = 'exhibition'


class Funding(models.Model):
    """
    Model for Funding table.
    """
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donor = models.ForeignKey('User', on_delete=models.SET_NULL, blank=True, null=True)
    artist = models.ForeignKey('User', on_delete=models.SET_NULL, blank=True, null=True, related_name='funding_artist_set')
    # date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'funding'


class Juryrequest(models.Model):
    """
    Model for Jurry request table.
    """
    applicant = models.ForeignKey('app3.User', on_delete=models.CASCADE)
    document_url = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=8, blank=True, null=True)
    # created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'juryrequest'


class Painting(models.Model):
    """
    Model for Painting table.
    """
    title = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.CharField(max_length=255)
    upload_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    artist = models.ForeignKey('User', models.DO_NOTHING)
    avg_rating = models.FloatField(blank=True, null=True)
    image_desc = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'painting'

    def get_average_rating(self):
        result = Rating.objects.filter(painting=self).aggregate(avg=Avg('score'))
        return result['avg'] or 0

class Participation(models.Model):
    """
    Model for Participation table.
    """
    pk = models.CompositePrimaryKey('painting_id', 'exhibition_id')
    painting = models.ForeignKey(Painting, on_delete=models.CASCADE)
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'participation'


class Rating(models.Model):
    """
    Model for Rating table.
    """
    score = models.IntegerField()
    # created_at = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey('app3.User', on_delete=models.CASCADE)
    painting = models.ForeignKey(Painting, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'rating'
        unique_together = (('author', 'painting'),)


class User(models.Model):
    """
    Model for User table.
    """
    username = models.CharField(unique=True, max_length=50)
    password_hash = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=100)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=10)
    bio = models.TextField(blank=True, null=True)
    # date_joined = models.DateTimeField(blank=True, null=True)
    pfp_url = models.TextField(blank=True, null=True)

    def is_regular_user(self):
        return self.role == 'registered'
    def is_jury(self):
        return self.role == 'jury'
    def is_admin(self):
        return self.role == 'admin'

    def __str__(self):
        return self.username
    def pfp_url_getter(self):
        if self.pfp_url:
            return self.pfp_url
        else: return '/static/img/default_pfp.png'
    class Meta:
        managed = False
        db_table = 'user'