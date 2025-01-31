from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from actual.views import ActualClientView
from actual.models import Actual
from media.models import Media
from appeals.models import Appeal
from actual.services import ActualService
from category.models import Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def MainPageClientView(request):
    # пагинация для обращений
    AppealPage = request.GET.get('page', 1)  
    appeals_per_page = int(request.GET.get('per_page', 8))
    appeals = Appeal.objects.all()  
    categories = Category.objects.all()
    appeal_paginator = Paginator(appeals, appeals_per_page)
    try:
        appeals_page = appeal_paginator.page(AppealPage)
    except PageNotAnInteger:
        appeals_page = appeal_paginator.page(1)
    appeals_all_pages = list(range(1, appeal_paginator.num_pages + 1))
    
    # пагинация для актуальных
    page = request.GET.get('page', 1)  
    per_page = int(request.GET.get('per_page', 5))
    actuals = Actual.objects.all()  
    paginator = Paginator(actuals, per_page)
    try:
        actual_page = paginator.page(page)
    except PageNotAnInteger:
        actual_page = paginator.page(1)
    all_pages = list(range(1, paginator.num_pages + 1))
    
    # pagination for gallery
    MediaPage = request.GET.get('page', 1)
    media_per_page = int(request.GET.get('per_page', 10))
    medias = Media.objects.all()
    media_paginator = Paginator(medias, media_per_page)
    try:
        media_page = media_paginator.page(MediaPage)
    except PageNotAnInteger:
        media_page = media_paginator.page(1)
    except EmptyPage:
        media_page = media_paginator.page(paginator.num_pages)
    media_all_pages = list(range(1, media_paginator.num_pages + 1))
    context = {
        "appeals": list(appeals_page.object_list.values()),  
        "AppealPage": appeals_page.number,
        "appeals_per_page": appeals_per_page,
        "appeals_total_pages": appeal_paginator.num_pages,
        "appeal_total_items": appeal_paginator.count,
        "appeals_all_pages": appeals_all_pages,
        "categories": categories,
        
        "medias": list(media_page.object_list.values()),  
        "MediaPage": media_page.number,
        "media_per_page": media_per_page,
        "media_total_pages": media_paginator.num_pages,
        "media_total_items": media_paginator.count,
        "media_all_pages": media_all_pages,
        "actuals": list(actual_page.object_list.values()),  
        "page": actual_page.number,
        "per_page": per_page,
        "total_pages": paginator.num_pages,
        "total_items": paginator.count,
        "all_pages": all_pages,
    }
    
    
    return render(request, "MainPage.html", context)
