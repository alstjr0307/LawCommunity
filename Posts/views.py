from django.core.paginator import Paginator
# Create your views here.
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView,CreateView,DeleteView,UpdateView
from .models import Post, Comment
from .forms import PostForm,CommentForm
from django.views.generic.edit import FormMixin
import datetime
from django.utils import timezone
from datetime import timedelta
from django.http import Http404
from .forms import PostForm
def time_elapsed_string(dt):
    """
    현재 시간과 비교하여 지난 시간을 분으로 환산하여 분 단위로 표시해주는 함수
    :param dt: datetime 객체 (UTC time)
    :return: str, '~분전' 형식의 문자열
    """
    diff = datetime.datetime.utcnow() - dt
    diff_in_minutes = diff.total_seconds() / 60.0

    if diff_in_minutes < 1:
        return '방금 전'
    elif diff_in_minutes < 60:
        return f'{int(diff_in_minutes)}분 전'
    elif diff_in_minutes < 24 * 60:
        return f'{int(diff_in_minutes // 60)}시간 전'
    else:
        return dt.strftime('%Y년 %m월 %d일 %H:%M:%S')

def delete_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        raise Http404('해당하는 게시물이 없습니다')
    if request.method == 'POST':
        password = request.POST['password']
        if post.delete_with_password(password):
            messages.success(request, '게시물이 삭제되었습니다.')
            return redirect('Posts:post_list')
        else:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
            return redirect('Posts:post_list', pk=pk)
    else:
        return render(request, 'Posts/delete_post.html', {'post': post})
    
    
def delete_comment(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        raise Http404('해당하는 댓글이 없습니다')
    if request.method == 'POST':
        password = request.POST['password']
        post_pk = comment.post.pk
        if comment.delete_with_password(password):
            messages.success(request, '댓글이 삭제되었습니다.')
            comment.is_deleted=True
            return redirect('Posts:post_detail', pk=post_pk)
        else:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
            return redirect('Posts:post_detail', pk=post_pk)
    else:
        raise Http404('잘못된 접근입니다.')


class CreatePostView(CreateView):
    model = Post
    fields = ['title', 'content', 'password', 'author',]
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
        for post in context['posts']:
            post_time = post.pub_date.replace(tzinfo=None)
            post.time = time_elapsed_string(post_time)
        return context
    
    
class DetailPostView(FormMixin, DetailView):
    model = Post
    template_name = 'Posts/detail_post.html'
    context_object_name = 'post'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
    
        context['comment_form'] = CommentForm()
        context['time'] = time_elapsed_string(post.pub_date.replace(tzinfo=None))
        comments = Comment.objects.filter(post=post).order_by('-pub_date')
        comment_list = []
        for comment in comments:
            comment_time = comment.pub_date.replace(tzinfo=None)
            comment.time = time_elapsed_string(comment_time)
            comment.id = comment.pk
            comment_list.append(comment)
            print(comment.id)
        context['comment_list'] = comment_list
        context['post_password'] = post.password
                
                
        return context  

    def get_success_url(self):
        return reverse_lazy('Posts:post_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.author_ip = self.request.META.get('HTTP_X_FORWARDED_FOR', self.request.META.get('REMOTE_ADDR'))
        self.object = self.get_object()
        comment = form.save(commit=False)
        comment.post = self.object
        comment.save()
        messages.success(self.request, '댓글이 성공적으로 작성되었습니다.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '댓글 작성에 실패하였습니다.')
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

        
class PostDeleteView(DetailView):
    model = Post
    success_url = reverse_lazy('Posts:post_list')
    template_name = 'Posts/post_confirm_delete.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        password = request.POST.get('password')
        if password == self.object.password:
            self.object.is_deleted = True
            self.object.save()
            return redirect(self.get_success_url())
        else:
            return self.get(self, request, *args, **kwargs)

    def form_invalid(self):
        return super().form_invalid()
    def get_success_url(self):
        return reverse_lazy('Posts:post_list')

from django.http import HttpResponseRedirect


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', ]
    template_name_suffix = '_update_form'
    def get_object(self): 
        post = get_object_or_404(Post, pk=self.kwargs['pk']) #4
        return post
    def form_valid(self, form):
        form.instance.author_ip = self.request.META.get('HTTP_X_FORWARDED_FOR', self.request.META.get('REMOTE_ADDR'))

        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('Posts:post_detail', kwargs={'pk': self.object.pk})
class CommentDeleteView(DetailView):
    model = Comment
    template_name = 'Posts/comment_confirm_delete.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        password = request.POST.get('password')

        if password == self.object.password:
            self.object.is_deleted = True
            self.object.save()
            return redirect(self.get_success_url())
        else:
            return self.get(self, request, *args, **kwargs)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER') or reverse_lazy('home')