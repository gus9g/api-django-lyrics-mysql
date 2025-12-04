from django.shortcuts import render
from lyrics_redirect_django.models import Band

def index(request):
    bands = Band.objects.order_by('nome')
    context = {'bands': bands}
    return render(request, 'site_client/index.html', context)
