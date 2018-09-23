from django.shortcuts import render

from .worth import *

def index(request):
    context = {
        'worth':worth(request),
    }
    return render(request, 'templates/resources/index.html', context)
