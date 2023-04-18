from django.views import View
from django.shortcuts import render
from django.views.generic import TemplateView

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
import os
from uuid import uuid4
from PIL import Image
...

@csrf_exempt
def upload_image(request):
    if request.method != "POST":
        return JsonResponse({'Error Message': "Wrong request"})

    # If it's not series and not article, handle it differently
  

    file_obj = request.FILES['file']
    file_name_suffix = file_obj.name.split(".")[-1]
    if file_name_suffix not in ["jpg", "png", "gif", "jpeg"]:
        return JsonResponse({"Error Message": f"Wrong file suffix ({file_name_suffix}), supported are .jpg, .png, .gif, .jpeg"})

    file_path = os.path.join(settings.MEDIA_ROOT, 'Posts', file_obj.name)
    
    if os.path.exists(file_path):
        file_obj.name = str(uuid4()) + '.' + file_name_suffix
        file_path = os.path.join(settings.MEDIA_ROOT, 'Posts', file_obj.name)

    with open(file_path, 'wb+') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
        with Image.open(file_path) as image:
            if image.width > 400:
                ratio = 400 / image.width
                height = int(image.height * ratio)
                image = image.resize((400, height))
                image.save(file_path)

        return JsonResponse({
            'message': 'Image uploaded successfully',
            'location': os.path.join(settings.MEDIA_URL, 'Posts',  file_obj.name)
        })    
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Welcome to Our Community!'
        return context