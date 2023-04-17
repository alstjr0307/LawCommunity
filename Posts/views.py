from django.core.paginator import Paginator
# Create your views here.
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView,CreateView
from .models import Post
from .forms import PostForm
class CreatePostView(CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'author',]

    template_name = 'Posts/create_post.html'
    success_url = reverse_lazy('Posts:post_list')

    def form_valid(self, form):
        form.instance.author_ip = self.request.META.get('HTTP_X_FORWARDED_FOR', self.request.META.get('REMOTE_ADDR'))

        return super().form_valid(form)
class ListPostView(ListView):
    model = Post
    template_name = 'Posts/list_post.html'
    context_object_name = 'posts'
    ordering = ['-pub_date']
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 현재 페이지 번호 가져오기
        page = self.request.GET.get('page')
        # 현재 페이지 번호에 해당하는 게시물 목록 가져오기
        paginator = Paginator(context['posts'], self.paginate_by)
        context['posts'] = paginator.get_page(page)
        return context
class DetailPostView(DetailView):
    model = Post
    template_name = 'Posts/detail_post.html'
    context_object_name = 'post'

