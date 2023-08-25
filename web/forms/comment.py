from django import forms
from web.models import Comment
from web.forms.bootstrap import BootStrapForm
from django.core.exceptions import ValidationError



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data['content']
        if not content:
            raise ValidationError('您还没有输入哦！暂且不能发布！')
        return content
