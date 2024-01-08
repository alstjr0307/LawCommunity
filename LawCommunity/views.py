from django.views import View
from django.shortcuts import render
from django.views.generic import TemplateView

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
import os
from uuid import uuid4
from PIL import Image
from Posts.models import Post
import boto3
...
@csrf_exempt  # Use csrf_exempt for simplicity in this example, consider using csrf token in production
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        # Handle the file upload and save it to your storage (S3 in your case)

        # Example using django-storages and boto3
        from storages.backends.s3boto3 import S3Boto3Storage
        from django.core.files.storage import default_storage

        class MediaStorage(S3Boto3Storage):
            location = 'media'
            file_overwrite = False

        # Save the file to your S3 bucket
        storage = MediaStorage()
        filename = storage.save(uploaded_file.name, uploaded_file)

        # Construct the URL to the saved image
        image_url = storage.url(filename)

        return JsonResponse({'location': image_url})
    else:
        return JsonResponse({'error': 'Invalid request'})
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.all().order_by('-pub_date')[:9]
        context['posts'] = posts
        context['message'] = 'Welcome to Our Community!'
        return context