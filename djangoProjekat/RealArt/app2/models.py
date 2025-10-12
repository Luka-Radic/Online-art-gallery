import datetime

from django.contrib.auth.models import User as DjangoUser
from django.db import models
from django.utils import timezone



def get_role(DjangoUser):
    users = User.objects.filter(username=DjangoUser.username)
    if users.count() != 0 and users.first() is not None:
        return users.first().role
    else:
        return ""
DjangoUser.get_role = get_role

class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    author = models.ForeignKey('User', models.DO_NOTHING)
    painting = models.ForeignKey('Painting', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'comment'


class Exhibition(models.Model):
    name = models.CharField(max_length=100)
    theme = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=6)
    created_by = models.ForeignKey('app2.User', models.DO_NOTHING, db_column='created_by')
    winner_painting = models.ForeignKey('Painting', models.DO_NOTHING, blank=True, null=True)

    def is_active(self):
        return self.start_date >= datetime.date.today() >= self.end_date

    class Meta:
        managed = False
        db_table = 'exhibition'


class Funding(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donor = models.ForeignKey('app2.User', models.DO_NOTHING)
    artist = models.ForeignKey('app2.User', models.DO_NOTHING, related_name='funding_artist_set')
    # date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'funding'


class Juryrequest(models.Model):
    applicant = models.ForeignKey('app2.User', models.DO_NOTHING)
    document_url = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=8, blank=True, null=True)
    # created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'juryrequest'


class Painting(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.CharField(max_length=255)
    upload_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    artist = models.ForeignKey('app2.User', models.DO_NOTHING)
    avg_rating = models.FloatField(blank=True, null=True)
    image_desc = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'painting'


class Participation(models.Model):
    pk = models.CompositePrimaryKey('painting_id', 'exhibition_id')
    painting = models.ForeignKey(Painting, models.DO_NOTHING)
    exhibition = models.ForeignKey(Exhibition, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'participation'


class Rating(models.Model):
    score = models.IntegerField()
    # created_at = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey('app2.User', models.DO_NOTHING)
    painting = models.ForeignKey(Painting, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'rating'
        unique_together = (('author', 'painting'),)


class User(models.Model):
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

    class Meta:
        managed = False
        db_table = 'user'