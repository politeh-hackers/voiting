import json

import uuid
from django.http import JsonResponse, HttpRequest
from django.views import View
from django.shortcuts import render

def BiographyClientView(request):
    return render(request, "biography.html")



    