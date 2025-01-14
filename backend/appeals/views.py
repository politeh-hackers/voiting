import json
from .models import Appeal
from .services import AppealService
import uuid
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def AppealsClientView(request: HttpRequest):
    page = request.GET.get('page', 1)  
    per_page = request.GET.get('per_page', 10) 
    appeals = Appeal.objects.all()  
    paginator = Paginator(appeals, per_page)
    try:
        appeals_page = paginator.page(page)
    except PageNotAnInteger:
        appeals_page = paginator.page(1)
    except EmptyPage:
        return JsonResponse({"error": "Page not found"}, status=404)
    context = {
        "appeals": list(appeals_page.object_list.values()),  
        "page": appeals_page.number,
        "per_page": per_page,
        "total_pages": paginator.num_pages,
        "total_items": paginator.count,
    }
    return render(request, "appeals.html", context)

<<<<<<< HEAD

=======
>>>>>>> bdcec7aaebdbeacc4be54b2ac67a555b34cca388
class AppealView(View):
    test_service = AppealService(model=Appeal)

    def get(self, request: HttpRequest):
        return JsonResponse(self.test_service.get_all(), safe=False)
    
    def post(self, request: HttpRequest):
        data = json.loads(request.body)
        # self.test_service.validate(data)
        self.test_service.create(data)
        return JsonResponse(None, safe=False)

    def delete(self, request: HttpRequest, model_id: uuid.UUID):
        self.test_service.delete(model_id=model_id)
        return JsonResponse(None, safe=False, status=204)

    def patch(self, request: HttpRequest, model_id: uuid.UUID):
        data = json.loads(request.body)
        # self.test_service.validate(data)
        self.test_service.update(model_id=model_id, data=data)
        return JsonResponse(None, safe=False)