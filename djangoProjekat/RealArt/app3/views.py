import os
import time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from RealArt import settings
from app3.models import *


def pocetna(request):
    return render(request, 'pocetna.html')


def adminUs(request):
    """
    Renders the admin page in which there are three functionalities. First is that admin user can approve jury requests from artist,
    which are only registered users. Second is that admin user can delete paintings from application. The third one is that admin
    user can delete commments from paintings on the application.
    """
    if request.method == "POST":
        akcija = request.POST['akcija']
        if akcija == "prihvati":
            request_id = request.POST['request_id']
            doc = Juryrequest.objects.filter(id=request_id).first()
            doc.status = Status.APPROVED
            doc.save()
            doc.applicant.role = Role.JURY
            doc.applicant.save()
        if akcija == "odbij":
            request_id = request.POST['request_id']
            Juryrequest.objects.filter(id=request_id).update(status=Status.REJECTED)
        if akcija == "brisanje":
            painting_id = request.POST['painting_id']
            if Painting.objects.filter(id=painting_id).exists():
                Painting.objects.get(id=painting_id).delete()
        if akcija == "brisanje_komentara":
            comment_id = request.POST['comment_id']
            if Comment.objects.filter(id=comment_id).exists():
                Comment.objects.filter(id=comment_id).delete()
        return redirect('adminUs')
    requests = Juryrequest.objects.filter(status=Status.PENDING)
    paintings = Painting.objects.all()
    comments = Comment.objects.all()
    context = {
        'requests': requests,
        'paintings': paintings,
        'comments': comments
    }

    return render(request, 'admin_stranica.html', context)


def exhibition(request, exhibition_id):
    """
    Renders a exhibition look page. It gives search bar, grid with all paintings which joined the exhibition, and later
    when its decided who is the winner, it shows the winner painting. Filters are done in JS because responsiveness.
    """
    izlozba = Exhibition.objects.get(id=exhibition_id)
    painting_ids = Participation.objects.filter(exhibition_id=exhibition_id).values_list('painting_id', flat=True)
    paintings = Painting.objects.filter(id__in=painting_ids)

    context = {
        'izlozba': izlozba,
        'paintings': paintings,
        'users': User.objects.all()
    }
    return render(request, 'prikaz_izlozbe.html', context)


def addPicture(request, exhibition_id):
    """
    This view is used for adding a painting on exhibition. Clicking on the exhibition add painting button, user is redirected to
    this view and needs to fill a form which is made from title, image and image description which is optional. After filling the
    form users gets redirected back to exhibition page.
    """
    izlozba = Exhibition.objects.get(id=exhibition_id)
    painting_ids = Participation.objects.filter(exhibition_id=exhibition_id).values_list('painting_id', flat=True)
    paintings = Painting.objects.filter(id__in=painting_ids)
    user = None
    if request.user.is_authenticated:
        user = User.objects.filter(username=request.user.username).first()

    if request.method == "POST" and request.FILES.get('image') is not None and user is not None:
        image = request.FILES.get('image')
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        if not title:
            messages.error(request, "Dodajte naziv slike")
            return redirect('exhibition', exhibition_id=exhibition_id)

        if image.content_type.startswith('image/'):
            base, ext = os.path.splitext(image.name)
            timestamp = int(time.time())
            filename = f"{base}_{timestamp}{ext}"
            path = os.path.join(settings.BASE_DIR, 'static', 'img', filename)

            with open(path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            image_url = f'/static/img/{filename}'
            new_painting = Painting.objects.create(
                title=title,
                image_url=image_url,
                artist=user,
                upload_date=timezone.now(),
                image_desc=description
            )
            Participation.objects.create(
                painting=new_painting,
                exhibition=izlozba
            )
            return redirect('exhibition', exhibition_id=exhibition_id)

    return render(request, 'dodaj_sliku.html')

@login_required
def chooseWinner(request, exhibition_id):
    """
    This view renders a form for choosing the winner after exhibition is done.
    """
    exhibition = Exhibition.objects.get(id=exhibition_id)

    if request.method == "POST":
        paintingId = request.POST['painting_id']
        painting = Painting.objects.get(id=paintingId)

        exhibition.winner_painting = painting
        exhibition.save()

    return redirect("exhibition", exhibition_id=exhibition.id)
def gallery(request):
    """
    Renders a gallery of all paintings published on the application.
    """
    data = []
    paintings = Painting.objects.all()
    for painting in paintings:
        themes = Participation.objects.filter(painting=painting).values_list('exhibition__theme', flat=True).distinct()
        data.append({
            'painting': painting,
            'themes': themes
        })
    context = {
        'paintings': data
    }
    return render(request, 'galerija.html', context)

def about(request):
    """
    Renders about us page.
    """
    return render(request, 'o_nama.html')