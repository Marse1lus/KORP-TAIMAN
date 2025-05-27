from django.urls import path
from . import views
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from .views import ReactionView

class BaseURLPatterns:
    def __init__(self, views, app_name):
        self.views = views
        self.app_name = app_name

    def get_urlpatterns(self):
        if self.app_name == 'kb':
            return [
                path('', self.views.article_list, name=f'{self.app_name}_list'),
                path('<int:pk>/', self.views.article_detail, name=f'{self.app_name}_detail'),
                path('create/', self.views.article_create, name=f'{self.app_name}_create'),
                path('<int:pk>/edit/', self.views.article_edit, name=f'{self.app_name}_edit'),
                path('<int:pk>/delete/', self.views.article_delete, name=f'{self.app_name}_delete'),
            ]
        elif self.app_name == 'news':
            return [
                path('', self.views.news_list, name=f'{self.app_name}_list'),
                path('<int:pk>/', self.views.news_detail, name=f'{self.app_name}_detail'),
                path('create/', self.views.news_create, name=f'{self.app_name}_create'),
                path('<int:pk>/edit/', self.views.news_edit, name=f'{self.app_name}_edit'),
                path('<int:pk>/delete/', self.views.news_delete, name=f'{self.app_name}_delete'),
            ]
        return []

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('profile/<int:pk>/edit/', views.edit_profile, name='edit_profile'),
    path('api/reactions/', ReactionView.as_view(), name='reactions_api'),
    
    # URLs для статей
    path('articles/', views.articles_list, name='articles_list'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('articles/create/', views.create_article, name='create_article'),
    path('article/<int:pk>/edit/', views.edit_article, name='edit_article'),
    path('article/<int:pk>/delete/', views.delete_article, name='delete_article'),
    
    # URLs для комментариев к статьям
    path('article/<int:article_id>/comment/<int:pk>/edit/', views.edit_comment, name='edit_comment'),
    path('article/<int:article_id>/comment/<int:pk>/delete/', views.delete_article_comment, name='delete_comment'),
    
    # URLs для новостей
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('news/create/', views.create_news, name='create_news'),
    path('news/<int:pk>/edit/', views.edit_news, name='edit_news'),
    path('news/<int:pk>/delete/', views.delete_news, name='delete_news'),
    
    # URLs для комментариев к новостям
    path('news/<int:news_id>/comment/<int:pk>/edit/', views.edit_news_comment, name='edit_news_comment'),
    path('news/<int:news_id>/comment/<int:pk>/delete/', views.delete_news_comment, name='delete_news_comment'),
    
    # URLs для альбомов
    path('albums/', views.event_albums_list, name='event_albums_list'),
    path('albums/<int:pk>/', views.event_album_detail, name='event_album_detail'),
    path('albums/create/', views.create_event_album, name='create_event_album'),
    path('albums/<int:pk>/edit/', views.edit_event_album, name='edit_event_album'),
    path('albums/<int:pk>/delete/', views.delete_event_album, name='delete_event_album'),
    
    # URLs для комментариев к альбомам
    path('albums/comment/<int:pk>/edit/', views.edit_event_comment, name='edit_event_comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

def user_logout(request):
    logout(request)
    return redirect('home')