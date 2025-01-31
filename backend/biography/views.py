import os
import json
from django.shortcuts import get_object_or_404
from gpt.views import generations_for_biography
from .models import Biography
from .services import BiographyService
import uuid
from .schemas import BiographySchema
from django.http import JsonResponse, HttpRequest
from django.views import View
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.views.generic import DetailView
class BiographyDetailView(DetailView):
    model = Biography
    template_name = "biography/biography_detail.html"  # Укажи свой шаблон
    context_object_name = "biography"  # Имя объекта в контексте

def BiographyClientView(request):
    return render(request, "biography.html")

class BiographyView(View):

    test_service = BiographyService(model=Biography)

    def get(self, request: HttpRequest):
        return JsonResponse(self.test_service.get_all(), safe=False)

    def post(self, request):
        data = request.POST.dict()
        validated_data = BiographySchema.model_validate(data).model_dump() 
        if data.get("h1") == "" or data.get("title") == "" or data.get("description") == "" or data.get("slug") == "":
            main_data = generations_for_biography(validated_data)
        else:
            main_data = data
        slug = main_data.get("slug")
        if slug:
            counter = 1
            original_slug = slug
            while Biography.objects.filter(slug=slug).exists():  
                slug = f"{original_slug}-{counter}" 
                counter += 1
            main_data["slug"] = slug 
        self.test_service.create(main_data)
        return JsonResponse({"message": "success"}, status=200)

    def delete(self, request: HttpRequest, model_id: uuid.UUID):
        media_instance = get_object_or_404(Biography, id=model_id)
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
        validated_data = BiographySchema.model_validate(data).model_dump() 
        generations_for_biography(data)
        self.test_service.update(model_id=model_id, data=validated_data)
        return JsonResponse(None, safe=False)

class ImageView(View):
    test_service = BiographyService(model=Biography) 

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
