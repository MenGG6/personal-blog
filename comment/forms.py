from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        #除了body外，其余的字段都可自动添加
        fields = ['body',]