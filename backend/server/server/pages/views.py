from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Appeal
from .models import Media


def home(request):
    return HttpResponse("<h1>ХУЙ</h1>")

def media(request):
    pass
"""

def get_all(request):
    return JsonResponse(list(Appeal.objects.all()), safe=False) #list[Appeals]

def create(request):
    import json

    body_unicode = request.body.decode('utf-8')  # Decode byte string to a Unicode string
    body_data = json.loads(body_unicode)
    my_new_model = Appeal.objects.create(**body_data)
"""

"""

def create(request):
    service = AppealService()
    body_unicode = request.body.decode('utf-8')  # Decode byte string to a Unicode string
    body_data = json.loads(body_unicode)
    
    service.create(body_data)
"""