
# Create your views here.
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from .models import Post, Comment
from .forms import PostForm, CommentForm

@method_decorator(login_required, name='dispatch')
class PostCreateView(View):
    form_class = PostForm
    template_name = 'community/post_form.html'

    def get(self, request):
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, '게시물이 성공적으로 작성되었습니다.')
            return redirect('post_detail', pk=post.pk)
        context = {'form': form}
        return render(request, self.template_name, context)
    
    
class PostDetailView(View):
    model = Post
    template_name = 'community/post_detail.html'

    def get(self, request, pk):
        post = self.model.objects.get(pk=pk)
        comments = post.comments.all()
        context = {'post': post, 'comments': comments}
        return render(request, self.template_name, context)