import json
import os
from django.shortcuts import get_object_or_404
from .models import Actual
from .services import ActualService 
import uuid
from django.http import JsonResponse, HttpRequest
from django.views import View
from django.core.handlers.wsgi import WSGIRequest
from .schemas import MediaActualFieldsSchema
from gpt.views import generations_for_news
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from telegram_bot.bot import send_news_to_telegram
from django.views.generic import DetailView
from category.views import Category
class ActualDetailView(DetailView):
    model = Actual
    template_name = "actual/actual_detail.html"  # Укажи свой шаблон
    context_object_name = "actual"  # Имя объекта в контексте

def ActualClientView(request: HttpRequest):
    popular_actuals = Actual.objects.order_by('-count')[:4]
    categories = Category.objects.all()
    page = request.GET.get('page', 1)  
    per_page = int(request.GET.get('per_page', 8))
    actuals = Actual.objects.all()  
    paginator = Paginator(actuals, per_page)
    try:
        actual_page = paginator.page(page)
    except PageNotAnInteger:
        actual_page = paginator.page(1)
    all_pages = list(range(1, paginator.num_pages + 1))
    context = {
        "popular_actuals":popular_actuals,
        "actuals": list(actual_page.object_list.values()),  
        "page": actual_page.number,
        "per_page": per_page,
        "total_pages": paginator.num_pages,
        "total_items": paginator.count,
        "all_pages": all_pages,
        "categories": categories
    }

    return render(request, "actual.html", context)

def ActualCard(request, slug: str):
    content = get_object_or_404(Actual, slug=slug)
    content.count += 1
    content.save()
    popular_actuals = Actual.objects.order_by('-count')[:3]
    content_data = json.loads(content.content)
    context = {
        "popular_actuals": popular_actuals,
        "content": content,
        "content_data": content_data, 
    }
    return render(request, "MediaPage.html", context)

class ActualView(View):

    test_service = ActualService(model=Actual)

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
            while Actual.objects.filter(slug=slug).exists():  
                slug = f"{original_slug}-{counter}" 
                counter += 1
            main_data["slug"] = slug 
        actual_instance: Actual = self.test_service.create(main_data)
        main_photo = os.path.join('static', 'image', actual_instance.main_photo)
        send_news_to_telegram(
            header=actual_instance.header,
            summary=actual_instance.summary,
            main_photo=main_photo,  
            url=f"http://localhost:8000/actual/{actual_instance.id}"  # Нужен публичный URL
        )
        return JsonResponse({"message": "success"}, status=200)

    def delete(self, request: HttpRequest, model_id: uuid.UUID):
        media_instance = get_object_or_404(Actual, id=model_id)
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

    def patch(self, request: HttpRequest, model_id: uuid.UUID):
        data = json.loads(request.body)
        validated_data = MediaActualFieldsSchema.model_validate(data).model_dump() 
        if (actual := Actual.objects.filter(id=model_id).first()) is not None and (actual.h1 == "" or actual.title == "" or actual.description == ""):
            main_data = generations_for_news(validated_data)
            self.test_service.update(model_id=model_id, data=main_data)
        self.test_service.update(model_id=model_id, data=validated_data)
        return JsonResponse(None, safe=False)

class ImageView(View):
    test_service = ActualService(model=Actual) 

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
