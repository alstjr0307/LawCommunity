"""
URL configuration for LawCommunity project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path
from .views import ListPostView, DetailPostView, CreatePostView,CommentDeleteView,PostDeleteView,PostUpdateView
from LawCommunity.views import upload_image

app_name = 'Posts'
urlpatterns = [
    path('', ListPostView.as_view(), name='post_list'),
    path('<int:pk>/', DetailPostView.as_view(), name='post_detail'),
    path('new/', CreatePostView.as_view(), name='post_new'),
    path('new/upload_image', upload_image, name="upload_image"),
    path('<int:pk>/', DetailPostView.as_view(), name='detail_post'),
    # 게시물 삭제
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post'),
    # 댓글 삭제
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='delete_comment'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
]