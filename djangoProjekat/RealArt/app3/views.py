import os
import time

from django.contrib import messages
from django.contrib.sites import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from RealArt import settings
from app3.models import *
def pocetna(request):
    return render(request, 'pocetna.html')

def adminUs(request):

    if request.method == "POST":
        akcija = request.POST['akcija']
        if akcija == "prihvati":
            request_id = request.POST['request_id']
            Juryrequest.objects.filter(id=request_id).update(status=Status.APPROVED)
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
        return redirect('odrzavanje')
    requests = Juryrequest.objects.filter(status=Status.PENDING)
    paintings = Painting.objects.all()
    comments = Comment.objects.all()
    context = {
        'requests' : requests,
        'paintings' : paintings,
        'comments' : comments
    }

    return render(request, 'admin_stranica.html', context)

def exhibition(request, exhibition_id):

    izlozba = Exhibition.objects.get(id=exhibition_id)
    painting_ids = Participation.objects.filter(exhibition_id=exhibition_id).values_list('painting_id', flat=True)
    paintings = Painting.objects.filter(id__in=painting_ids)
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)

    if request.method == "POST" and request.FILES.get('image'):
        image = request.FILES.get('image')
        title = request.POST.get('title', '').strip()

        if not title:
            messages.error(request, "Dodajte naziv slike")
            return redirect('exhibition', exhibition_id=exhibition_id)

        if image.content_type.startswith('image/'):
            base, ext = os.path.splitext(image.name)
            timestamp = int(time.time())
            filename = f"{base}_{timestamp}{ext}"
            path = os.path.join(settings.BASE_DIR,'static', 'img', filename)

            with open(path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            image_url = f'/static/img/{filename}'
            new_painting = Painting.objects.create(
                title = title,
                image_url = image_url,
                artist = user,
                upload_date = timezone.now(),
            )
            Participation.objects.create(
                painting=new_painting,
                exhibition=izlozba
            )
            return redirect(reverse('exhibition', args=[exhibition_id]))
    context = {
        'izlozba' : izlozba,
        'paintings' : paintings,
        'users' : User.objects.all()
    }
    return render(request, 'prikaz_izlozbe.html', context)