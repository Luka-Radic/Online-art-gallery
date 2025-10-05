from django.contrib.sites import requests
from django.shortcuts import render, redirect

from app3.models import *
def pocetna(request):
    return render(request, 'pocetna.html')

def odrzavanje(request):

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
    paintings = Painting.objects.all();
    comments = Comment.objects.all();
    context = {
        'requests' : requests,
        'paintings' : paintings,
        'comments' : comments
    }

    return render(request, 'admin_stranica.html', context)