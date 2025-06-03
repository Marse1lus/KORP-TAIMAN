from django.db import models 
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.cache import cache
from django.db.models import Count
from albums.models import EventAlbum, EventPhoto, EventComment
from app.reactions import Reaction, ReactionMixin

class User(AbstractUser):
	photo = models.ImageField(upload_to='photos/', blank=True, null=True)
	position = models.CharField(max_length=255, blank=True)
	department = models.CharField(max_length=255, blank=True)
	bio = models.TextField(blank=True)

	groups = models.ManyToManyField(
		Group,
		related_name='custom_user_set',
		blank=True,
		help_text='The groups this user belongs to.',
		verbose_name='groups',
	)
	user_permissions = models.ManyToManyField(
		Permission,
		related_name='custom_user_set',
		blank=True,
		help_text='Specific permissions for this user.',
		verbose_name='user permissions',
	)

class KnowledgeCategory(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.name

class KnowledgeArticle(ReactionMixin, models.Model):
	title = models.CharField(max_length=255)
	content = models.TextField()
	published_at = models.DateTimeField(auto_now_add=True, null=True)
	is_published = models.BooleanField(default=False)
	category = models.ForeignKey(KnowledgeCategory, on_delete=models.CASCADE, related_name='articles')
	author = models.ForeignKey('app.User', on_delete=models.CASCADE, related_name='knowledge_articles')
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	dislikes = models.IntegerField(default=0)
	image = models.ImageField(upload_to='article_images/', blank=True, null=True)
	attachment = models.FileField(upload_to='article_files/', blank=True, null=True)

	def __str__(self):
		return self.title

class NewsCategory(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.name
	
class KnowledgeComment(models.Model):
    article = models.ForeignKey(KnowledgeArticle, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('app.User', on_delete=models.CASCADE, related_name='knowledge_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)