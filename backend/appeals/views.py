import json
import base64
from .schemas import AppealCreateSchema, AppealUpdateSchema
from .models import Appeal
from .services import AppealService
import uuid
from django.http import JsonResponse, HttpRequest, request
from django.views import View
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger
from gpt.views import generations_for_appeals
import os
from django.core.handlers.wsgi import WSGIRequest
from category.models import Category
from telegram_bot.bot import send_appeal_to_telegram
from django.core.files.uploadedfile import InMemoryUploadedFile
from typing import cast
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from PIL import Image
from io import BytesIO

class AppealDetailView(DetailView):
    model = Appeal
    template_name = "appeals/appeal_detail.html"  # Укажи свой шаблон
    context_object_name = "appeal"  # Имя объекта в контексте

class AppealsClientView(View):
    test_service = AppealService(model=Appeal)
    
    def get(self, request):
        page = request.GET.get('page', 1)  
        per_page = int(request.GET.get('per_page', 3))
        appeals = Appeal.objects.filter(on_website=True)  
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
            "categories": categories
        }
        return render(request, "appeals.html", context)


class AppealView(View):
    test_service = AppealService(model=Appeal)

    def get(self, request: HttpRequest):
        return JsonResponse(self.test_service.get_all(), safe=False)
    
    def post(self, request: HttpRequest):
        data = json.loads(request.body)
        category_name = data.get('category')
        if (category := Category.objects.filter(name=category_name).first()) is not None:
            data["category"] = category.name 
        validated_data: dict = AppealCreateSchema.model_validate(data).model_dump()
        if not data.get("h1") or not data.get("title") or not data.get("description") or not data.get("slug") :
            main_data = generations_for_appeals(validated_data)
        else:
            main_data = data
        slug = main_data.get("slug")
        if slug:
            counter = 1
            original_slug = slug
            while Appeal.objects.filter(slug=slug).exists():  
                slug = f"{original_slug}-{counter}" 
                counter += 1
            main_data["slug"] = slug
        self.test_service.create(main_data)
        return JsonResponse(None, safe=False)

    def delete(self, request: HttpRequest, model_id: uuid.UUID):
        self.test_service.delete(model_id=model_id)
        return JsonResponse(None, safe=False, status=204)

    def patch(self, request: HttpRequest, model_id: uuid.UUID):
        data = json.loads(request.body)
        category_name = data.get("category")
        if (category := Category.objects.filter(name=category_name).first()) is not None:
            data["category"] = category.name 
        validated_data: dict = AppealUpdateSchema.model_validate(data).model_dump()
        appeal_instance = Appeal.objects.filter(id=model_id).first()
        self.test_service.update(model_id=model_id, data=validated_data)
        if data.get("status") == "Исполнено":
            send_appeal_to_telegram(
                category=appeal_instance.category,
                date=appeal_instance.date, 
                url=f"http://localhost:8000/appeals/{appeal_instance.id}"
                )

        return JsonResponse(None, safe=False)


class ImageView(View):
    test_service = AppealService(model=Appeal) 

    def get(self, request: HttpRequest):
        return JsonResponse(self.test_service.get_all(), safe=False)
        
    def post(self, request:WSGIRequest):
        if "photos" in request.FILES:
            images = request.FILES.getlist("photos") 
            print(request.FILES)
        else:
            return JsonResponse({"error": "No images provided"}, status=400)
        image_dir = os.path.join('static/image')
        os.makedirs(image_dir, exist_ok=True)
        saved_photos = []  
        for data in images:
            file_name = str(data)
            image_path = os.path.join(image_dir, file_name)
            base_name, extension = os.path.splitext(file_name)
            counter = 1
            while os.path.exists(image_path):  
                file_name = f"{base_name}_{counter}{extension}"
                image_path = os.path.join(image_dir, file_name)
                counter += 1
            with open(image_path, 'wb') as image_file:
                for chunk in data.chunks():
                    image_file.write(chunk)
            saved_photos.append(f"http://localhost:8000/static/image/{file_name}")

        return JsonResponse({"photos": saved_photos, "message": "Photos uploaded successfully"}, safe=False)

    def delete(self, request: HttpRequest, file_name: str):
        image_path = os.path.join('static/image', file_name)
        if os.path.exists(image_path):
            os.remove(image_path)
        return JsonResponse(None, safe=False)
