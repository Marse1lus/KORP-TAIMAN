from django import forms
from app.models import KnowledgeArticle, KnowledgeComment, EventAlbum, EventPhoto
from news_app.models import News, NewsComment
from albums.models import PhotoComment
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()

class KnowledgeArticleForm(forms.ModelForm):
	class Meta:
		model = KnowledgeArticle
		fields = ['title', 'content', 'category', 'image']

class KnowledgeCommentForm(forms.ModelForm):
	class Meta:
		model = KnowledgeComment
		fields = ['content']

class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
	username = forms.CharField(label='Имя Пользователя')
	password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class ProfileEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name', 'photo', 'position', 'department', 'bio']

# class NewsCommentForm(forms.ModelForm):
# 	class Meta:
# 		model = NewsComment
# 		fields = ['text']

class EventAlbumForm(forms.ModelForm):
	class Meta:
		model = EventAlbum
		fields = ['title', 'description', 'event_date']
		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
			'event_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
		}

class EventPhotoForm(forms.ModelForm):
	class Meta:
		model = EventPhoto
		fields = ['photo', 'caption']

