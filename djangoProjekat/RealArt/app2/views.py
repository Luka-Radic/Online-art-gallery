import random

from django.shortcuts import render, redirect, get_object_or_404
from .forms import ExhibitionForm
from .models import Exhibition, Painting, Participation


def add_exhibition(request):
    if request.method == 'POST':
        form = ExhibitionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('izlozbe_lista')  # kasnije ćemo dodati ovaj prikaz
    else:
        form = ExhibitionForm()
    return render(request, 'izlozbe.html', {'form': form})

def exhibitions(request):
    if request.method == 'POST':
        form = ExhibitionForm(request.POST)
        if form.is_valid():
            print(form.theme)
            izlozba = form.save(commit=False)
            izlozba.save()
            return redirect('exhibitions')
    else:
        form = ExhibitionForm()

    izlozbe = Exhibition.objects.all()

    izlozbe_sa_slikom = []
    for iz in izlozbe:
        radovi = Participation.objects.filter(exhibition=iz)
        if radovi.exists():
            slika = random.choice(radovi).painting.image_url
        else:
            slika = '/static/img/mona_lisa.webp'
        broj_radova = Participation.objects.filter(exhibition=iz).count()
        umetnici = Participation.objects.filter(exhibition=iz).values('painting__artist').distinct().count()
        izlozbe_sa_slikom.append({
            'izlozba': iz,
            'slika': slika,
            'broj_radova': broj_radova,
            'broj_umetnika': umetnici
        })

    context = {
        'form': form,
        'izlozbe_sa_slikom': izlozbe_sa_slikom
    }
    return render(request, 'izlozbe.html', context)

def image_detail(request, painting_id):
    painting = get_object_or_404(Painting, id=painting_id)
    # kasnije dodaj komentare
    comments = []  # placeholder
    return render(request, 'slika.html', {'painting': painting, 'comments': comments})
