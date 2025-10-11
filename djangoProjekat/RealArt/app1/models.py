from datetime import datetime
from django.db import models

# Create your models here.

class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    painting = models.ForeignKey('Painting', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'comment'


class Exhibition(models.Model):
    name = models.CharField(max_length=100)
    theme = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=6)
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, blank=True, null=True, db_column='created_by')
    winner_painting = models.ForeignKey('Painting', on_delete=models.SET_NULL, blank=True, null=True)

    def is_active(self):
        return self.start_date >= datetime.date.today() >= self.end_date

    class Meta:
        managed = True
        db_table = 'exhibition'


class Funding(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donor = models.ForeignKey('User', on_delete=models.SET_NULL, blank=True, null=True,)
    artist = models.ForeignKey('User', on_delete=models.SET_NULL, blank=True, null=True, related_name='funding_artist_set')
    # date = models.DateTimeField(blank=True, null=True) da bi sam dodelio datum u bazi sa current timestampom

    class Meta:
        managed = True
        db_table = 'funding'


class Juryrequest(models.Model):
    applicant = models.ForeignKey('User',  on_delete=models.CASCADE)
    document_url = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'juryrequest'


class Painting(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.CharField(max_length=255)
    artist = models.ForeignKey('User',  on_delete=models.CASCADE)
    avg_rating = models.FloatField(blank=True, null=True)
    image_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'painting'


class Participation(models.Model):
    pk = models.CompositePrimaryKey('painting_id', 'exhibition_id')
    painting = models.ForeignKey(Painting, on_delete=models.CASCADE)
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'participation'


class Rating(models.Model):
    score = models.IntegerField()
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    painting = models.ForeignKey(Painting, on_delete=models.CASCADE)

    class Meta:
        managed = True
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
    pfp_url = models.CharField(max_length=255, blank=True, null=True)

    def get_funding(self):
        fundings = Funding.objects.filter(artist_id=self.id)
        sum = 0
        for f in fundings:
            sum += f.amount
        return sum

    def get_rating(self):
        my_paintings = Painting.objects.filter(artist_id=self.id)
        avg = 0
        num = 0

        for painting in my_paintings:
            ratings = Rating.objects.filter(painting_id=painting.id)
            for r in ratings:
                avg += r.score
                num += 1

        if num != 0:
            return avg/num
        else:
            return 0


    def get_qualification_url(self):
        qualifications = Juryrequest.objects.filter(applicant_id=self.id).first()
        if qualifications:
            return qualifications.document_url
        return '/static/user_docs/default_doc.txt'


    def is_regular_user(self):
        return self.role == 'registered'
    def is_jury(self):
        return self.role == 'jury'
    def is_admin(self):
        return self.role == 'admin'

    class Meta:
        managed = True
        db_table = 'user'
