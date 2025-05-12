from django import forms
from app.models import KnowledgeArticle, KnowledgeComment, User, News, NewsComment, EventAlbum, EventPhoto, PhotoComment
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
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

class NewsForm(forms.ModelForm):
	class Meta:
		model = News
		fields = ['title', 'content', 'category', 'image', 'attachment', 'is_published']

class NewsCommentForm(forms.ModelForm):
	class Meta:
		model = NewsComment
		fields = ['text']

class EventAlbumForm(forms.ModelForm):
	class Meta:
		model = EventAlbum
		fields = ['title', 'description']

class EventPhotoForm(forms.ModelForm):
	class Meta:
		model = EventPhoto
		fields = ['photo', 'caption']

class PhotoCommentForm(forms.ModelForm):
	class Meta:
		model = PhotoComment
		fields = ['text']
		

