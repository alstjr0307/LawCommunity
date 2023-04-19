from django import forms
from .models import Post
from .models import Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from tinymce.widgets import TinyMCE
class PostForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(render_value=False,attrs={'placeholder': '********'}))

    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'password', 'author_ip']

class CommentForm(forms.ModelForm):
    content = forms.CharField(label='댓글', widget=forms.Textarea(attrs={'rows': 3}))
    password = forms.CharField(widget=forms.PasswordInput(), required=True, max_length=128, label="비밀번호")

    class Meta:
        model = Comment
        fields = ['author', 'content', 'password']
        widgets = {
            'author': forms.TextInput(attrs={'placeholder': '작성자'}),
        }
        
        # crispy_forms 라이브러리 적용
        helper = FormHelper()
        helper.form_method = 'post'
        helper.layout = Layout(
            Row(
                Column('author', css_class='form-group col-md-6 mb-0'),
                Column('password', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'content',
            Submit('submit', '댓글 작성', css_class='btn btn-primary'),
        )
