from django.urls import path
from . import views
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
	path('articles/', views.articles_list, name='articles_list'),
	path('articles/create/', views.create_article, name='create_article'),
    path('articles/<int:pk>/edit/', views.edit_article, name='edit_article'),
    path('articles/<int:pk>/delete/', views.delete_article, name='delete_article'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('comment/<int:pk>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('profile/<int:pk>/edit/', views.edit_profile, name='edit_profile'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('news/create/', views.create_news, name='create_news'),
    path('news/<int:pk>/edit/', views.edit_news, name='edit_news'),
    path('news/<int:pk>/delete/', views.delete_news, name='delete_news'),
    path('news/<int:news_id>/comment/add/', views.add_news_comment, name='add_news_comment'),
    path('news/comment/<int:pk>/edit/', views.edit_news_comment, name='edit_news_comment'),
    path('news/comment/<int:pk>/delete/', views.delete_news_comment, name='delete_news_comment'),
    path('albums/', views.event_albums_list, name='event_albums_list'),
    path('albums/create/', views.create_event_album, name='create_event_album'),
    path('albums/<int:pk>/', views.event_album_detail, name='event_album_detail'),
    path('albums/<int:pk>/add_photo/', views.add_event_photo, name='add_event_photo'),
    path('albums/<int:pk>/add_comment/', views.add_event_comment, name='add_event_comment'),
    path('photo/<int:photo_id>/add_comment/', views.add_photo_comment, name='add_photo_comment'),
    path('albums/<int:pk>/like/', views.like_album, name='like_album'),
    path('albums/<int:pk>/dislike/', views.dislike_album, name='dislike_album'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

def user_logout(request):
    logout(request)
    return redirect('home')