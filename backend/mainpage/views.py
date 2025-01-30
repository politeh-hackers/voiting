from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from actual.views import ActualClientView
from actual.models import Actual
from actual.services import ActualService
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def MainPageClientView(request):
    page = request.GET.get('page', 1)  
    per_page = int(request.GET.get('per_page', 3))
    actuals = Actual.objects.all()  
    paginator = Paginator(actuals, per_page)
    try:
        actual_page = paginator.page(page)
    except PageNotAnInteger:
        actual_page = paginator.page(1)
    all_pages = list(range(1, paginator.num_pages + 1))
    context = {
        "actuals": list(actual_page.object_list.values()),  
        "page": actual_page.number,
        "per_page": per_page,
        "total_pages": paginator.num_pages,
        "total_items": paginator.count,
        "all_pages": all_pages,
    }
    return render(request, "MainPage.html", context)
