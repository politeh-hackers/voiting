from asyncio.windows_events import NULL
import json
import os
from django.shortcuts import get_object_or_404
from .schemas import MediaActualFieldsSchema
from .models import Media
from .services import MediaService
import uuid
from django.http import JsonResponse, HttpRequest
from django.views import View
from django.core.handlers.wsgi import WSGIRequest
from gpt.views import generations_for_news
from telegram_bot.bot import send_news_to_telegram
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def MediaClientView(request: HttpRequest):
# pagination for gallery
    page = request.GET.get('page', 1)
    per_page = int(request.GET.get('per_page', 5))
    medias = Media.objects.all()  # Получаем все объекты модели
    paginator = Paginator(medias, per_page)

    try:
        media_page = paginator.page(page)
    except PageNotAnInteger:
        media_page = paginator.page(1)
    except EmptyPage:
        media_page = paginator.page(paginator.num_pages)
# pagination for left cards
    page1 = request.GET.get('page1', 1)
    additional_data_1 = Media.objects.all()  # Замените на вашу модель
    per_page1 = int(request.GET.get('per_page', 2))
    paginator1 = Paginator(additional_data_1, per_page1)
    try:
        data_page_1 = paginator1.page(page1)
    except PageNotAnInteger:
        data_page_1 = paginator1.page(1)
    except EmptyPage:
        data_page_1 = paginator1.page(paginator1.num_pages)
# paginatoin for main cards
    page2 = request.GET.get('page2', 1)
    additional_data_2 = Media.objects.all()  # Замените на вашу модель
    per_page2 = int(request.GET.get('per_page', 8))
    paginator2 = Paginator(additional_data_2, per_page2)
    try:
        data_page_2 = paginator2.page(page2)
    except PageNotAnInteger:
        data_page_2 = paginator2.page(1)
    except EmptyPage:
        data_page_2 = paginator2.page(paginator2.num_pages)
    context = {
        "additional_data_1": data_page_1,
        "additional_data_2": data_page_2,
        "data1_total_pages": paginator1.num_pages,
        "data1_total_items": paginator1.count,
        "data2_total_pages": paginator2.num_pages,
        "data2_total_items": paginator2.count,
        "medias": media_page,  # Передаем объекты, а не список значений
        "page": media_page.number,
        "page1": data_page_1.number,
        "page2" : data_page_2.number,
        "per_page": per_page,
        "per_page1": per_page1,
        "per_page2": per_page2,
        "total_pages": paginator.num_pages,
        "total_pages1": paginator.num_pages,
        "total_pages2": paginator.num_pages,
        "total_items": paginator.count,
        "all_pages": list(paginator.page_range),
        "all_pages2": list(paginator1.page_range),
        "all_pages3":list(paginator2.page_range)
    }

    return render(request, "media.html", context)
    
class MediaView(View):

    test_service = MediaService(model=Media)

    def get(self, request: HttpRequest):
        return JsonResponse(self.test_service.get_all(), safe=False)

    def post(self, request):
        data = request.POST.dict()
        validated_data = MediaActualFieldsSchema.model_validate(data).model_dump()
        if data.get("h1") == "" or data.get("title") == "" or data.get("description") == "":
            main_data = generations_for_news(validated_data)
            media_instance: Media = self.test_service.create(main_data)
        else:
            media_instance: Media = self.test_service.create(data)
        main_photo = os.path.join('static', 'image', media_instance.main_photo)
        send_news_to_telegram(
            header=media_instance.header,
            summary=media_instance.summary,
            main_photo=main_photo,  
            url=f"http://localhost:8000/media/{media_instance.id}" #нужен публичный url
        )
        return JsonResponse({"message": "success"}, status=200)

    def delete(self, request: HttpRequest, model_id: uuid.UUID):
        media_instance = get_object_or_404(Media, id=model_id)
        main_photo = media_instance.main_photo
        if main_photo:
            main_photo_path = os.path.join('static/image', main_photo)
            if os.path.exists(main_photo_path):
                os.remove(main_photo_path)
        content = media_instance.content
        if content:
            for block in json.loads(content).get("blocks", []):
                if block.get("type") == "image":
                    file_name = block["data"]["file"]["name"]
                    image_path = os.path.join('static/image', file_name)
                    if os.path.exists(image_path):
                        os.remove(image_path)
        self.test_service.delete(model_id=model_id)
        return JsonResponse(None, safe=False)

    def patch(self, request, model_id: uuid.UUID):
        data: dict = json.loads(request.body)
        validated_data: dict = MediaActualFieldsSchema.model_validate(data).model_dump()
        if (media := Media.objects.filter(id=model_id).first()) is not None and (media.h1 == "" or media.title == "" or media.description == ""):
            main_data = generations_for_news(validated_data)
            self.test_service.update(model_id=model_id, data=main_data)
        else:
            self.test_service.update(model_id=model_id, data=validated_data)
        return JsonResponse(None, safe=False)
        
class ImageView(View):
    test_service = MediaService(model=Media) 

    def get(self, request: HttpRequest):
        return JsonResponse(self.test_service.get_all(), safe=False)

    def post(self, request: WSGIRequest):
        if "main_photo" in request.FILES:
            data = request.FILES["main_photo"]
        elif "image" in request.FILES:
            data = request.FILES["image"]
        else:
            return JsonResponse({"error": "No image provided"}, status=400)
        file_name = str(data)
        image_dir = os.path.join('static/image')
        os.makedirs(image_dir, exist_ok=True)  
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
                return JsonResponse(
                {
                    "url": f"http://localhost:8000/static/image/{file_name}",
                    "name": file_name,
                    "size": data.size,
                    "type": data.content_type
                }, safe=False)

    def delete(self, request: HttpRequest, file_name: str):
        image_path = os.path.join('static/image', file_name)
        if os.path.exists(image_path):
            os.remove(image_path)
        return JsonResponse(None, safe=False)
