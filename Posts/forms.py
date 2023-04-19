from django import forms
from .models import Post
from .models import Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from tinymce.widgets import TinyMCE
class PostForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    password = forms.CharField(max_length=12, widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'password', 'author_ip']

class CommentForm(forms.ModelForm):
    content = forms.CharField(label='댓글', widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Comment
        fields = ['author', 'content', 'password']

