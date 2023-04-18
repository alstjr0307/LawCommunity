from django import forms
from .models import Post
from .models import Comment
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'author', 'author_ip']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'author_ip': forms.HiddenInput(),
        }

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class CommentForm(forms.ModelForm):
    content = forms.CharField(label='댓글', widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Comment
        fields = ['author', 'content']
        widgets = {
            'author': forms.TextInput(attrs={'placeholder': '작성자'}),
        }
        
        # crispy_forms 라이브러리 적용
        helper = FormHelper()
        helper.form_method = 'post'
        helper.layout = Layout(
            Row(
                Column('author', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'content',
            Submit('submit', '댓글 작성', css_class='btn btn-primary'),
        )