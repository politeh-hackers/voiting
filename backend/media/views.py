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
from django.http import Http404
from django.views.generic import DetailView
from actual.models import Actual
from category.models import Category
class MediaDetailView(DetailView):
    model = Media
    template_name = "media/media_detail.html"  # Укажи свой шаблон
    context_object_name = "media"  # Имя объекта в контексте

def MediaClientView(request: HttpRequest):
# pagination for gallery
    page = request.GET.get('page', 1)
    per_page = int(request.GET.get('per_page', 8))
    medias = Media.objects.all()[3:]  # Получаем все объекты модели
    paginator = Paginator(medias, per_page)
    try:
        media_page = paginator.page(page)
    except PageNotAnInteger:
        media_page = paginator.page(1)
    except EmptyPage:
        media_page = paginator.page(paginator.num_pages)
# pagination for left cards
    page1 = request.GET.get('page1', 1)
    medias1 = Media.objects.all() 
    categories = Category.objects.all()
    per_page1 = int(request.GET.get('per_page1', 3))
    paginator1 = Paginator(medias1, per_page1)
    try:
        media_page1 = paginator1.page(page1)
    except PageNotAnInteger:
        media_page1 = paginator1.page(1)
    except EmptyPage:
        media_page1 = paginator1.page(paginator1.num_pages)

    context = {
        "categories": categories,
        "medias1": media_page1,
        "total_items2": paginator1.count,
        "medias": media_page,  # Передаем объекты, а не список значений
        "page": media_page.number,
        "page1": media_page1.number,
        "per_page": per_page,
        "per_page1": per_page1,
        "total_pages": paginator.num_pages,
        "total_pages1": paginator1.num_pages,
        "total_items": paginator.count,
        "all_pages": list(paginator.page_range),
        "all_pages2": list(paginator1.page_range),
    }
    
    return render(request, "media.html", context)

def MediaCard(request, model_id: uuid.UUID):
    content = get_object_or_404(Media, id=model_id)
    content.count += 1
    popular_actuals = Actual.objects.order_by('-count')[:3]
    content.save()
    content_data = json.loads(content.content)
    
    context = {
        "popular_actuals":popular_actuals,
        "content": content,
        "content_data": content_data  # Если нужно передать и JSON данные тоже
    }
    
    return render(request, "MediaPage.html", context)

class MediaView(View):

    test_service = MediaService(model=Media)

    def get(self, request: HttpRequest):
        return JsonResponse(self.test_service.get_all(), safe=False)

    def post(self, request):
        data = request.POST.dict()
        validated_data: dict = MediaActualFieldsSchema.model_validate(data).model_dump()
        if data.get("h1") == "" or data.get("title") == "" or data.get("description") == "" or data.get("slug") == "":
            main_data = generations_for_news(validated_data)
        else:
            main_data = data
        slug = main_data.get("slug")
        if slug:
            counter = 1
            original_slug = slug
            while Media.objects.filter(slug=slug).exists():  
                slug = f"{original_slug}-{counter}" 
                counter += 1
            main_data["slug"] = slug 
        media_instance: Media = self.test_service.create(main_data)
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
