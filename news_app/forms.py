from django import forms
from .models import News, NewsComment

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'image', 'attachment', 'is_published']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        } 

class NewsCommentForm(forms.ModelForm):
    class Meta:
        model = NewsComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введите комментарий...'}),
        } 