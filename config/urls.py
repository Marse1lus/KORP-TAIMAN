from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app.views import (
	NewsCategoryList, NewsList, NewsDetail, 
	NewsCommentList, RegisterView, TokenObtainPairView, 
	TokenRefreshView, ReactionView, NewsCommentDetail, 
	KnowledgeCategoryList, KnowledgeArticleList, KnowledgeArticleDetail,
	KnowledgeCommentList, KnowledgeCommentDetail
)
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
	path('api/', include([
		path('news-categories/', NewsCategoryList.as_view(), name='news-category-list'),
		path('news/', NewsList.as_view(), name='news-list'),
		path('news/<int:pk>/', NewsDetail.as_view(), name='news-detail'),
		path('news/comments/', NewsCommentList.as_view(), name='news-comment-list'),
		path('news/comments/<int:pk>/', NewsCommentDetail.as_view(), name='news-comment-detail'),
		path('register/', RegisterView.as_view(), name='register'),
		path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
		path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
		path('reactions/', ReactionView.as_view(), name='reaction-list'),
		path('knowledge-categories/', KnowledgeCategoryList.as_view(), name='knowledge-category-list'),
		path('knowledge-articles/', KnowledgeArticleList.as_view(), name='knowledge-article-list'),
		path('knowledge-articles/<int:pk>/', KnowledgeArticleDetail.as_view(), name='knowledge-article-detail'),
		path('knowledge-articles/<int:article_id>/comments/', KnowledgeCommentList.as_view(), name='knowledge-comment-list'),
		path('knowledge-articles/<int:article_id>/comments/<int:comment_id>/', KnowledgeCommentDetail.as_view(), name='knowledge-comment-detail'),
	])),
	path('', include('app.urls')),
	path('kb/', include('kb.urls')),
	path('news/', include('news_app.urls')),
	path('albums/', include('albums.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

