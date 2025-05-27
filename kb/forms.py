from django import forms
from app.models import KnowledgeArticle

class ArticleForm(forms.ModelForm):
    class Meta:
        model = KnowledgeArticle
        fields = ['title', 'content', 'image', 'attachment']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        } 