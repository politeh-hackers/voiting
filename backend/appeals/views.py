import json
from .schemas import AppealFieldsSchema
from .models import Appeal
from .services import AppealService
import uuid
from django.http import JsonResponse, HttpRequest
from django.views import View
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger
from gpt.views import generations_for_appeals
from category.models import Category

def AppealsClientView(request: HttpRequest):
    page = request.GET.get('page', 1)  
    per_page = int(request.GET.get('per_page', 3))
    appeals = Appeal.objects.all()  
    categories = Category.objects.all()
    paginator = Paginator(appeals, per_page)
    try:
        appeals_page = paginator.page(page)
    except PageNotAnInteger:
        appeals_page = paginator.page(1)
    all_pages = list(range(1, paginator.num_pages + 1))
    context = {
        "appeals": list(appeals_page.object_list.values()),  
        "page": appeals_page.number,
        "per_page": per_page,
        "total_pages": paginator.num_pages,
        "total_items": paginator.count,
        "all_pages": all_pages,
        "categories": categories,
    }
    
    return render(request, "ModalAppeals.html", context)


class AppealView(View):
    test_service = AppealService(model=Appeal)

    def get(self, request: HttpRequest):
        return JsonResponse(self.test_service.get_all(), safe=False)
    
    def post(self, request: HttpRequest):
        data = json.loads(request.body)
        validated_data: dict = AppealFieldsSchema.model_validate(data).model_dump()
        main_data = generations_for_appeals(validated_data)
        self.test_service.create(main_data)
        return JsonResponse(None, safe=False)

    def delete(self, request: HttpRequest, model_id: uuid.UUID):
        self.test_service.delete(model_id=model_id)
        return JsonResponse(None, safe=False, status=204)

    def patch(self, request: HttpRequest, model_id: uuid.UUID):
        data = json.loads(request.body)
        # self.test_service.validate(data)
        self.test_service.update(model_id=model_id, data=data)
        return JsonResponse(None, safe=False)