from rest_framework import serializers
from .models import User, KnowledgeCategory, KnowledgeArticle, KnowledgeComment, NewsCategory, News, NewsComment, EventAlbum, EventPhoto, EventComment
from .models import Reaction

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username', 'email', 'first_name', 'last_name', 'photo', 'position', 'department', 'bio']

class KnowledgeCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = KnowledgeCategory
		fields = ['id', 'name', 'description']

class KnowledgeArticleSerializer(serializers.ModelSerializer):
	class Meta:
		model = KnowledgeArticle
		fields = ['id','title', 'content', 'published_at', 'is_published', 'category', 'author', 'views', 'likes', 'dislikes']
		read_only_fields = ['author', 'views', 'likes', 'dislikes', 'published_at']
		
class KnowledgeCommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = KnowledgeComment
		fields = ['id', 'article', 'author', 'content', 'created_at']
		read_only_fields = ['article', 'author', 'created_at']


class NewsCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = NewsCategory
		fields = ['id', 'name', 'description']

class NewsSerializer(serializers.ModelSerializer):
	class Meta:
		model = News
		fields = ['id', 'title', 'content', 'published_date', 'is_published', 'category','author', 'views', 'likes', 'dislikes']
 
class NewsCommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = NewsComment
		fields = ['id', 'news', 'author', 'text', 'created_at', 'likes', 'dislikes']

class EventAlbumSerializer(serializers.ModelSerializer):
	class Meta:
		model = EventAlbum
		fields = ['id', 'title', 'description', 'event_date', 'likes', 'dislikes']

class EventPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPhoto
        fields = ['id', 'album', 'photo', 'caption', 'uploaded_at', 'author']

class EventCommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = EventComment
		fields = ['id', 'album', 'author', 'text', 'created_at', ]


class ReactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Reaction
		fields = ['id', 'user', 'content_type', 'object_id', 'reaction_type', 'created_at']
		read_only_fields = ['user', 'created_at']
		