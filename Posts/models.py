from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField 
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=8, default='익명')
    author_ip = models.CharField(max_length=15)
    

    def __str__(self):
        return self.title

    def summary(self):
        return self.content[:100]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=8)
    author_ip = models.CharField(max_length=15)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content