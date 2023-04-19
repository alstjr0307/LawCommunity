from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField 
from django.urls import reverse
class Post(models.Model):
    title = models.CharField(max_length=20)
    content = HTMLField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=8)
    author_ip = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)
    def delete_with_password(self, password):
        if self.password == password:
            self.is_deleted= True
            return True
        return False

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
    password = models.CharField(max_length=100, null=True, blank=True)
    is_deleted = models.BooleanField(default=False) 
    def delete_with_password(self, password):
        if self.password == password:
            self.is_deleted=True
            return True
        return False
    def __str__(self):
        return self.content
    def get_absolute_url(self):
        return reverse('comment_delete', kwargs={'pk': self.pk})