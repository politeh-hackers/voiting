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
from gpt.services import generations_for_news
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

def ActualClientView(request: HttpRequest):
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

    return render(request, "actual.html", context)
class ActualView(View):

    test_service = ActualService(model=Actual)

    def get(self, request: HttpRequest):
        return JsonResponse(self.test_service.get_all(), safe=False)

    def post(self, request):
        data = request.POST.dict()
        validated_data = MediaActualFieldsSchema.model_validate(data).model_dump() 
        generations_for_news(data)
        self.test_service.create(validated_data)
        # self.test_service.create(data)
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
