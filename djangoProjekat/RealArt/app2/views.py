import random
from datetime import date, datetime, timezone

from django.shortcuts import render, redirect, get_object_or_404
from .forms import ExhibitionForm
from .models import Exhibition, Painting, Participation, User, Comment, Rating
from django.contrib.auth.models import User as DjangoUser
from django.db.models import Avg

#def add_exhibition(request):
    #if request.method == 'POST':
        #form = ExhibitionForm(request.POST)
        #if form.is_valid():
            #form.save()
            #return redirect('izlozbe_lista')  # kasnije ćemo dodati ovaj prikaz
   # else:
        #form = ExhibitionForm()
    #return render(request, 'izlozbe.html', {'form': form})


#Ovde se prave izlzobe, stavlja se njivo status adekvatno
def exhibitions(request):
    # Automatsko ažuriranje statusa svih izložbi
    today = date.today()
    for iz in Exhibition.objects.all():
        new_status = "active" if iz.start_date <= today <= iz.end_date else "closed"
        if iz.status != new_status:
            iz.status = new_status
            iz.save()

    # Kreiranje nove izložbe
    if request.method == 'POST':
        form = ExhibitionForm(request.POST)
        if form.is_valid():
            izlozba = form.save(commit=False)
            izlozba.created_by = User.objects.filter(username=request.user.username).first()
            izlozba.status = "active" if izlozba.start_date <= today <= izlozba.end_date else "closed"
            izlozba.winner_painting = None
            izlozba.save()
            return redirect('exhibitions')
    else:
        form = ExhibitionForm()

    izlozbe_sa_slikom = []
    for iz in Exhibition.objects.all():
        radovi = Participation.objects.filter(exhibition=iz)
        slika = random.choice(radovi).painting.image_url if radovi.exists() else '/static/img/mona_lisa.webp'
        umetnici = radovi.values('painting__artist').distinct().count()
        izlozbe_sa_slikom.append({
            'izlozba': iz,
            'slika': slika,
            'broj_radova': radovi.count(),
            'broj_umetnika': umetnici
        })

    return render(request, 'izlozbe.html', {'form': form, 'izlozbe_sa_slikom': izlozbe_sa_slikom})


#ovde je sve sto ima veze sa slikom, dodavanje komentara, dodavanje ocene korisnika i atomatsko azuriranje prosecne ocene
def image_detail(request, painting_id):
    painting = get_object_or_404(Painting, id=painting_id)

    app2_user = None
    if request.user.is_authenticated:
        app2_user = User.objects.filter(username=request.user.username).first()

    if request.method == 'POST' and app2_user:
        # Dodavanje komentara
        text = request.POST.get('comment_text', '').strip()
        if text:
            Comment.objects.create(
                text=text,
                painting=painting,
                author=app2_user,
                created_at=datetime.now()
            )
            return redirect('image_detail', painting_id=painting.id)

        # Dodavanje/azuriranje ocene
        rating_value = request.POST.get('rating_value')
        if rating_value:
            rating_value = int(rating_value)
            existing_rating = Rating.objects.filter(painting=painting, author=app2_user).first()
            if existing_rating:
                if existing_rating.score == rating_value:
                    existing_rating.delete()  # klik na istu ocenu -> briše
                else:
                    existing_rating.score = rating_value
                    existing_rating.created_at = datetime.now()
                    existing_rating.save()
            else:
                Rating.objects.create(
                    painting=painting,
                    author=app2_user,
                    score=rating_value,
                    created_at=datetime.now()
                )
            return redirect('image_detail', painting_id=painting.id)

    # komentari
    comments = Comment.objects.filter(painting=painting).order_by('-created_at')

    # Prosečna ocena
    avg_rating = Rating.objects.filter(painting=painting).aggregate(Avg('score'))['score__avg']
    avg_rating = round(avg_rating or 0, 2)

    # Korisnikova ocena
    user_rating = None
    if app2_user:
        existing_rating = Rating.objects.filter(painting=painting, author=app2_user).first()
        if existing_rating:
            user_rating = existing_rating.score

    # Zvezdice
    stars = [1, 2, 3, 4, 5]

    return render(request, 'slika.html', {
        'painting': painting,
        'comments': comments,
        'avg_rating': avg_rating,
        'user_rating': user_rating,
        'stars': stars
    })






