from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from app.models import (
	KnowledgeCategory, KnowledgeArticle, KnowledgeComment,
	NewsCategory, News, NewsComment,
	EventAlbum, EventPhoto, EventComment, Reaction
)
from .serializer import (
	KnowledgeCategorySerializer, KnowledgeArticleSerializer, KnowledgeCommentSerializer,
	NewsCategorySerializer, NewsSerializer, NewsCommentSerializer,
	EventAlbumSerializer, EventPhotoSerializer, EventCommentSerializer, ReactionSerializer
)
from .serializer import UserSerializer 

from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
User = get_user_model() 

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework.pagination import PageNumberPagination
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from rest_framework.generics import ListCreateAPIView
from config.permission import IsAuthor
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import render
from app.forms import LoginForm, UserRegistrationForm, KnowledgeArticleForm, KnowledgeCommentForm, ProfileEditForm, NewsForm, NewsCommentForm, EventAlbumForm, EventPhotoForm, PhotoCommentForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import LoginForm, UserRegistrationForm
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from django.http import HttpResponseForbidden

class CustomPagination(PageNumberPagination):
	page_size = 10
	page_size_query_param = 'page_size'
	max_page_size = 100

class KnowledgeArticleList(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		articles = KnowledgeArticle.objects.all()
		category_id = request.query_params.get('category')
		if category_id:
			articles = articles.filter(category_id=category_id)
		serializer = KnowledgeArticleSerializer(articles, many=True)
		return Response(serializer.data) 
	
	def post(self, request):
		serializer = KnowledgeArticleSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(author=request.user)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			print(serializer.errors)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KnowledgeArticleDetail(APIView):
	permission_classes = [IsAuthenticatedOrReadOnly]

	def get(self,request, pk):
		article = get_object_or_404(KnowledgeArticle, pk=pk)
		serializer = KnowledgeArticleSerializer(article)
		return Response(serializer.data)
	
	def put(self, request, pk):
		article = get_object_or_404(KnowledgeArticle, pk=pk)
		if article.author != request.user:
			return Response(status=status.HTTP_403_FORBIDDEN)
		serializer = KnowledgeArticleSerializer(article, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, pk):
		article = get_object_or_404(KnowledgeArticle, pk=pk)
		if article.author != request.user:
			return Response({'detail': 'Вы не являетесь автором этой статьи'}, status=status.HTTP_403_FORBIDDEN)
		article.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class KnowledgeCategoryList(APIView):
	permission_classes = [IsAuthenticatedOrReadOnly]

	def get(self, request):
		categories = KnowledgeCategory.objects.all()
		serializer = KnowledgeCategorySerializer(categories, many=True)
		return Response(serializer.data)
	
	def post(self, request):
		serializer = KnowledgeCategorySerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
class KnowledgeCategoryDetail(APIView):
	permission_classes = [IsAdminUser] 

	def get(self, request, pk):
		category = get_object_or_404(KnowledgeCategory,pk=pk)
		serializer = KnowledgeCategorySerializer(category)
		return Response(serializer.data)
		
	def put(self, request, pk):
		category = get_object_or_404(KnowledgeCategory,pk=pk)
		serializer = KnowledgeCategorySerializer(category, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, pk):
		category = get_object_or_404(KnowledgeCategory,pk=pk)
		category.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
	
class NewsCategoryList(APIView):
	permission_classes = [IsAuthenticatedOrReadOnly]

	def get(self, request):
		categories = NewsCategory.objects.all()
		serializer = NewsCategorySerializer(categories,many=True)
		return Response(serializer.data)
		
	def post(self, request):
		serializer = NewsCategorySerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
class NewsList(APIView):
	permission_classes = [IsAuthenticated]
	pagination_class = CustomPagination

	def get(self, request):
		news = News.objects.all()
		category_id = request.query_params.get('category')
		if category_id:
			news = news.filter(category_id=category_id)
			
		paginator = self.pagination_class()
		paginated_news = paginator.paginate_queryset(news, request)
		serializer = NewsSerializer(paginated_news, many=True)
		return paginator.get_paginated_response(serializer.data)

	def post(self, request):
		serializer = NewsSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(author=request.user)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsDetail(APIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]

	def put(self, request, pk):
		news_item = get_object_or_404(News, pk=pk)
		
		if news_item.author != request.user:
			return Response(
				{'detail': 'Вы не являетесь автором этой новости'},
				status=status.HTTP_403_FORBIDDEN
			)

		serializer = NewsSerializer(news_item, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk):
		news_item = get_object_or_404(News, pk=pk)
		news_item.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class NewsCommentList(APIView):
	permission_classes = [IsAuthenticatedOrReadOnly]

	def get(self, request):
		news_id = request.query_params.get('news')
		comments = NewsComment.objects.filter(news_id=news_id)
		serializer = NewsCommentSerializer(comments, many=True)
		return Response(serializer.data)

	def post(self, request):
		serializer = NewsCommentSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(author=request.user)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	

class NewsCommentDetail(APIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request, pk):
		comment = get_object_or_404(NewsComment, pk=pk)
		serializer = NewsCommentSerializer(comment)
		return Response(serializer.data)

	def put(self, request, pk):
		comment = get_object_or_404(NewsComment, pk=pk)
		
		if comment.author != request.user:
			return Response(
				{'detail': 'Вы не являетесь автором этого комментария'},
				status=status.HTTP_403_FORBIDDEN
			)
		
		serializer = NewsCommentSerializer(comment, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, pk):
		comment = get_object_or_404(NewsComment, pk=pk)
		if comment.author != request.user:
			return Response(
				{'detail': 'ты же ле не автор чтоб удалять'},
				status=status.HTTP_403_FORBIDDEN
			)
		
		comment.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

	
class EventPhotoList(APIView):
	permission_classes = [IsAuthenticatedOrReadOnly]

	def get(self, request):
		photos = EventPhoto.objects.all()
		album_id = request.query_params.get('album')
		if album_id:
			photos = photos.filter(album_id=album_id)
		serializer = EventPhotoSerializer(photos, many=True)
		return Response(serializer.data)
	
	def post(self, request):
		serializer = EventPhotoSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(author=request.user)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
class EventAlbumList(APIView):
	permission_classes = [IsAuthenticatedOrReadOnly]

	def get(self, request):
		albums = EventAlbum.objects.all()
		serializer = EventAlbumSerializer(albums, many=True)
		return Response(serializer.data)

	def post(self, request):
		serializer = EventAlbumSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(author=request.user)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
class EventCommentList(APIView):
	permission_classes = [IsAuthenticatedOrReadOnly]

	def get(self, request):
		album_id = request.query_params.get('album')
		comments = EventComment.objects.filter(album_id=album_id)
		serializer = EventCommentSerializer(comments, many=True)
		return Response(serializer.data)
		
	def post(self, request):
		serializer = EventCommentSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(author=request.user)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
class UserList(APIView):
	permission_classes = [IsAuthenticatedOrReadOnly] 	

	def get(self, request):
		users = User.objects.all()
		serializer = UserSerializer(users, many=True)
		return Response(serializer.data)

class UserDetail(APIView):
	permission_classes = [IsAuthenticatedOrReadOnly]

	def get(self, request, pk):
		user = get_object_or_404(User, pk=pk)
		serializer = UserSerializer(user)
		return Response(serializer.data)
	
	def put(self, request, pk):
		if request.user.pk != pk:
			return Response(
				{'detail': 'Вы можете редактировать только свой профиль'},
				status=status.HTTP_403_FORBIDDEN
			)
		user = get_object_or_404(User, pk=pk)
		serializer = UserSerializer(user, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
class RegisterView(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():

			password = request.data.get('password')
			try:
				validate_password(password)
			except Exception as e:
				return Response({'password': str(e)}, status=status.HTTP_400_BAD_REQUEST)
			
			email = request.data.get('email')
			if User.objects.filter(email=email).exists():
				return Response(
					{'email': 'Пользователь с таким email уже существует'},
					status=status.HTTP_400_BAD_REQUEST
				)
			
			user = serializer.save()
			user.set_password(password)
			user.save()

			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReactionView(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request):
		serializer = ReactionSerializer(data=request.data)
		if serializer.is_valid():
			try:
			
				content_type_value = request.data.get('content_type')
				if content_type_value.isdigit():
					content_type = ContentType.objects.get(id=content_type_value)
				else:
					content_type = ContentType.objects.get(model=content_type_value.lower())
				
				model = content_type.model_class()
			
				obj = model.objects.get(id=request.data.get('object_id'))
			except (ContentType.DoesNotExist, model.DoesNotExist):
				return Response(
					{'error': 'Объект не найден'},
					status=status.HTTP_404_NOT_FOUND
				)


			reaction, created = Reaction.objects.update_or_create(
				user=request.user,
				content_type=content_type,
				object_id=obj.id,
				defaults={'reaction_type': serializer.validated_data['reaction_type']}
			)


			obj.likes = Reaction.objects.filter(
				content_type=content_type,
				object_id=obj.id,
				reaction_type=Reaction.LIKE
			).count()
			obj.dislikes = Reaction.objects.filter(
				content_type=content_type,
				object_id=obj.id,
				reaction_type=Reaction.DISLIKE
			).count()
			obj.save()

			return Response({
				'likes': obj.likes,
				'dislikes': obj.dislikes,
				'object_id': obj.id,
				'content_type': content_type.id,
			})
		else:
			print(serializer.errors)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request):
		
	
		content_type_name = request.data.get('content_type')
		object_id = request.data.get('object_id')
			
		if not all([content_type_name, object_id]):
			return Response(
				{'error': 'Укажите content_type и object_id'},
				status=status.HTTP_400_BAD_REQUEST
			)

		model = News if content_type_name == 'news' else NewsComment
		content_type = ContentType.objects.get_for_model(model)

		try:
			reaction = Reaction.objects.get(
				user=request.user,
				content_type=content_type,
				object_id=object_id
			)
		except Reaction.DoesNotExist:
			return Response(status=status.HTTP_204_NO_CONTENT)

		
		obj = model.objects.get(id=object_id)
		reaction.delete()

		
		obj.likes = Reaction.objects.filter(
			content_type=content_type,
			object_id=obj.id,
			reaction_type=Reaction.LIKE
		).count()
		obj.dislikes = Reaction.objects.filter(
			content_type=content_type,
			object_id=obj.id,
			reaction_type=Reaction.DISLIKE
		).count()
		obj.save()

		return Response(status=status.HTTP_204_NO_CONTENT)

class KnowledgeCommentList(APIView):
	permission_classes = [IsAuthenticatedOrReadOnly]

	def get(self, request, article_id):
		article = get_object_or_404(KnowledgeArticle, pk=article_id)
		comments = KnowledgeComment.objects.filter(article=article)
		serializer = KnowledgeCommentSerializer(comments, many=True)
		return Response(serializer.data)

	def post(self, request, article_id):
		article = get_object_or_404(KnowledgeArticle, pk=article_id)
		serializer = KnowledgeCommentSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(author=request.user, article=article)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class KnowledgeCommentDetail(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request, article_id, comment_id):
		article = get_object_or_404(KnowledgeArticle, pk=article_id)
		comment = get_object_or_404(KnowledgeComment, pk=comment_id, article=article)
		serializer = KnowledgeCommentSerializer(comment)
		return Response(serializer.data)

	def put(self, request, article_id, comment_id):
		article = get_object_or_404(KnowledgeArticle, pk=article_id)
		comment = get_object_or_404(KnowledgeComment, pk=comment_id, article=article)
		
		if comment.author != request.user:
			return Response(
				{'detail': 'Вы не являетесь автором этого комментария'},
				status=status.HTTP_403_FORBIDDEN
			)
		
		serializer = KnowledgeCommentSerializer(comment, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, article_id, comment_id):
		article = get_object_or_404(KnowledgeArticle, pk=article_id)
		comment = get_object_or_404(KnowledgeComment, pk=comment_id, article=article)
		
		if comment.author != request.user:
			return Response(
				{'detail': 'Вы не являетесь автором этого комментария'},
				status=status.HTTP_403_FORBIDDEN
			)
		
		comment.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

def home(request):
	category_id = request.GET.get('category')
	search_query = request.GET.get('q')
	categories = KnowledgeCategory.objects.all()

	articles = KnowledgeArticle.objects.all()
	if category_id:
		articles = KnowledgeArticle.objects.filter(category_id=category_id)
	if search_query:
		articles =articles.filter(title__icontains=search_query)

	return render(request, 'app/home.html',{
		'articles': articles,
		'categories': categories,
		'selected_category': int(category_id) if category_id else None,
		'search_query': search_query,
	})

def article_detail(request, pk):
	article = get_object_or_404(KnowledgeArticle, pk=pk)
	comments = KnowledgeComment.objects.filter(article=article)
	article_type_id = ContentType.objects.get_for_model(KnowledgeArticle).id
	comment_type_id = ContentType.objects.get_for_model(KnowledgeComment).id

	if request.method == 'POST' and request.user.is_authenticated:
		form = KnowledgeCommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.article = article
			comment.author = request.user
			comment.save()
			return redirect('article_detail', pk=pk)
	else:
		form = KnowledgeCommentForm()

	return render(request, 'app/article_detail.html', {
        'article': article,
        'comments': comments,
        'form': form,
        'article_type_id': article_type_id,
        'comment_type_id': comment_type_id,
    })

def articles_list(request):
	from app.models import KnowledgeArticle, KnowledgeCategory
	articles = KnowledgeArticle.objects.all()
	categories = KnowledgeCategory.objects.all()
	return render(request, 'app/articles_list.html',{
		'articles': articles,
		'categories': categories,
		})

@login_required
def create_article(request):
	if request.method == 'POST':
		form = KnowledgeArticleForm(request.POST, request.FILES)
		if form.is_valid():
			article = form.save(commit=False)
			article.author = request.user
			article.save()
			return redirect('articles_list')
	else:
		form = KnowledgeArticleForm()
	
	return render(request, 'app/create_article.html', {'form': form})

def edit_article(request, pk):
	article = get_object_or_404(KnowledgeArticle, pk=pk)
	if request.method == 'POST':
		form = KnowledgeArticleForm(request.POST, request.FILES, instance=article)
		if form.is_valid():
			form.save()
			return redirect('article_detail', pk=article.pk)
	else:
		form = KnowledgeArticleForm(instance=article)
	return render(request, 'app/edit_article.html',{'form': form, 'article': article})

def user_login(request):
	if request.method == 'POST':
		form = LoginForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect('home')
	else:
		form = LoginForm()
	return render(request, 'app/login.html', {'form': form})

def user_logout(request):
	logout(request)
	return redirect('home')

def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('home')
	else:
		form = UserRegistrationForm()
	return render(request, 'app/register.html', {'form': form})

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(KnowledgeComment, pk=pk)
    if request.user != comment.author:
        return HttpResponseForbidden("Вы не можете редактировать этот комментарий.")
    if request.method == 'POST':
        form = KnowledgeCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('article_detail', pk=comment.article.pk)
    else:
        form = KnowledgeCommentForm(instance=comment)
    return render(request, 'app/edit_comment.html', {'form': form, 'comment': comment})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(KnowledgeComment, pk=pk)
    if request.user != comment.author:
        return HttpResponseForbidden("Вы не можете удалить этот комментарий.")
    article_pk = comment.article.pk
    if request.method == 'POST':
        comment.delete()
        return redirect('article_detail', pk=article_pk)
    return render(request, 'app/delete_comment.html', {'comment': comment})

@login_required
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    articles = user.knowledge_articles.all()
    comments = user.knowledge_comments.all()
    return render(request, 'app/profile.html', {
        'profile_user': user,
        'articles': articles,
        'comments': comments,
    })

@login_required
def edit_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.user != user:
        return HttpResponseForbidden("Вы не можете редактировать этот профиль.")
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.pk)
    else:
        form = ProfileEditForm(instance=user)
    return render(request, 'app/edit_profile.html', {'form': form, 'profile_user': user})

def news_list(request):
    news = News.objects.all().order_by('-published_date')
    return render(request, 'app/news_list.html', {'news': news})

def news_detail(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    comments = NewsComment.objects.filter(news=news_item)
    return render(request, 'app/news_detail.html', {'news_item': news_item, 'comments': comments})

@login_required
def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return redirect('news_detail', pk=news.pk)
    else:
        form = NewsForm()
    return render(request, 'app/news_form.html', {'form': form})

@login_required
def edit_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.user != news.author:
        return HttpResponseForbidden("Вы не можете редактировать эту новость.")
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news_detail', pk=news.pk)
    else:
        form = NewsForm(instance=news)
    return render(request, 'app/news_form.html', {'form': form, 'news': news})

@login_required
def delete_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.user != news.author:
        return HttpResponseForbidden("Вы не можете удалить эту новость.")
    if request.method == 'POST':
        news.delete()
        return redirect('news_list')
    return render(request, 'app/news_confirm_delete.html', {'news': news})

@login_required
def add_news_comment(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
    if request.method == 'POST':
        form = NewsCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news_item
            comment.author = request.user
            comment.save()
            return redirect('news_detail', pk=news_id)
    else:
        form = NewsCommentForm()
    return render(request, 'app/news_comment_form.html', {'form': form, 'news_item': news_item})

@login_required
def edit_news_comment(request, pk):
    comment = get_object_or_404(NewsComment, pk=pk)
    if request.user != comment.author:
        return HttpResponseForbidden("Вы не можете редактировать этот комментарий.")
    if request.method == 'POST':
        form = NewsCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('news_detail', pk=comment.news.pk)
    else:
        form = NewsCommentForm(instance=comment)
    return render(request, 'app/news_comment_form.html', {'form': form, 'news_item': comment.news})

@login_required
def delete_news_comment(request, pk):
    comment = get_object_or_404(NewsComment, pk=pk)
    if request.user != comment.author:
        return HttpResponseForbidden("Вы не можете удалить этот комментарий.")
    news_pk = comment.news.pk
    if request.method == 'POST':
        comment.delete()
        return redirect('news_detail', pk=news_pk)
    return render(request, 'app/news_comment_confirm_delete.html', {'comment': comment})

@login_required
def delete_article(request, pk):
    article = get_object_or_404(KnowledgeArticle, pk=pk)
    if request.user != article.author:
        return HttpResponseForbidden("Вы не можете удалить эту статью.")
    if request.method == 'POST':
        article.delete()
        return redirect('articles_list')
    return render(request, 'app/article_confirm_delete.html', {'article': article})

def is_moderator(user):
    return user.groups.filter(name='Модератор').exists() or user.is_superuser

@user_passes_test(is_moderator)
def moderate_comment(request, pk):
    pass

def event_albums_list(request):
    albums = EventAlbum.objects.all().order_by('-event_date')
    return render(request, 'app/event_albums_list.html', {'albums': albums})

def event_album_detail(request, pk):
    album = get_object_or_404(EventAlbum, pk=pk)
    photos = album.photos.all()
    comments = album.comments.all()
    album_type_id = ContentType.objects.get_for_model(EventAlbum).id
    photo_type_id = ContentType.objects.get_for_model(EventPhoto).id
    return render(request, 'app/event_album_detail.html', {
        'album': album,
        'photos': photos,
        'comments': comments,
        'album_type_id': album_type_id,
        'photo_type_id': photo_type_id,
    })

@login_required
def create_event_album(request):
    if request.method == 'POST':
        form = EventAlbumForm(request.POST)
        if form.is_valid():
            album = form.save()
            return redirect('event_album_detail', pk=album.pk)
    else:
        form = EventAlbumForm()
    return render(request, 'app/create_event_album.html', {'form': form})

@login_required
def add_event_photo(request, pk):
    album = get_object_or_404(EventAlbum, pk=pk)
    if request.method == 'POST':
        files = request.FILES.getlist('photo')
        for f in files:
            EventPhoto.objects.create(album=album, author=request.user, photo=f)
        return redirect('event_album_detail', pk=album.pk)
    else:
        form = EventPhotoForm()
    return render(request, 'app/add_event_photo.html', {'form': form, 'album': album})

@login_required
def add_event_comment(request, pk):
    album = get_object_or_404(EventAlbum, pk=pk)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            EventComment.objects.create(album=album, author=request.user, text=text)
            return redirect('event_album_detail', pk=album.pk)
    return render(request, 'app/add_event_comment.html', {'album': album})

@login_required
def add_photo_comment(request, photo_id):
    photo = get_object_or_404(EventPhoto, pk=photo_id)
    if request.method == 'POST':
        form = PhotoCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.photo = photo
            comment.author = request.user
            comment.save()
            return redirect('event_album_detail', pk=photo.album.pk)
    else:
        form = PhotoCommentForm()
    return render(request, 'app/add_photo_comment.html', {'form': form, 'photo': photo})

@login_required
def like_album(request, pk):
    album = get_object_or_404(EventAlbum, pk=pk)
    album.likes += 1
    album.save()
    return redirect('event_album_detail', pk=pk)

@login_required
def dislike_album(request, pk):
    album = get_object_or_404(EventAlbum, pk=pk)
    album.dislikes += 1
    album.save()
    return redirect('event_album_detail', pk=pk)