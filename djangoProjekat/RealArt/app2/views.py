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
            izlozba.created_by = User.objects.filter(username=DjangoUser.username).first()
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


def image_detail(request, painting_id):
    painting = get_object_or_404(Painting, id=painting_id)

    app2_user = None
    if request.user.is_authenticated:
        app2_user = User.objects.filter(username=request.user.username).first()

    # POST: komentar ili rating
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

    # Dohvati komentare
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


def rate_painting(request, painting_id):
    """
    Prima POST zahtev sa ocenom i čuva je u bazi podataka za prijavljenog korisnika.
    """

    # 1. Provera metode zahteva (Ekvivalent @require_POST)
    if request.method != 'POST':
        # Vraća HTTP 405 Method Not Allowed ako nije POST
        return HttpResponse('Method Not Allowed', status=405)

    # 2. Provera statusa prijave (Ekvivalent @login_required)
    if not request.user.is_authenticated:
        # Vraća HTTP 401 Unauthorized ako korisnik nije prijavljen
        # U AJAX pozivu je bolje vratiti status greške nego preusmeriti.
        return JsonResponse({'error': 'Korisnik nije prijavljen. Prijavite se za ocenjivanje.'}, status=401)

    # --- Nastavak logike ocenjivanja ---

    painting = get_object_or_404(Painting, id=painting_id)

    try:
        data = json.loads(request.body)
        score = data.get('score')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Neispravan JSON format'}, status=400)

    if not score or not (1 <= score <= 5):
        return JsonResponse({'error': 'Ocena mora biti između 1 i 5'}, status=400)

    # Koristi get_or_create da pronađe postojeći ili kreira novi rating
    rating, created = Rating.objects.update_or_create(
        author=request.user,  # Trenutno prijavljeni korisnik
        painting=painting,
        defaults={
            'score': score,
            # 'created_at' bi trebalo da se podesi u modelu kao auto_now_add,
            # ali kako je `managed = False`, možda ćete morati ručno da ga podesite
        }
    )

    # Izračunavanje nove prosečne ocene
    avg_rating = Rating.objects.filter(painting=painting).aggregate(Avg('score'))['score__avg']

    # Vraćanje JSON odgovora klijentu
    return JsonResponse({
        'message': 'Ocena uspešno sačuvana',
        'score': rating.score,
        'created': created,
        'avg_rating': round(avg_rating, 2) if avg_rating is not None else 0
    })




