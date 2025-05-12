from django.db import models 
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.cache import cache
from django.db.models import Count

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
	
class ReactionMixin:
	def get_cache_key(self):
		return f'reactions_{self.__class__.__name__.lower()}_{self.id}'
		
	def get_reactions_count(self):
	
		cache_key = self.get_cache_key()
		cached_data = cache.get(cache_key)
		
		if cached_data is not None:
			return cached_data
			

		content_type = ContentType.objects.get_for_model(self)
		counts = Reaction.objects.filter(
			content_type=content_type,
			object_id=self.id
		).values('reaction_type').annotate(
			count=Count('id')
		)
		
		result = {
			Reaction.LIKE: 0,
			Reaction.DISLIKE: 0
		}
		
		for item in counts:
			result[item['reaction_type']] = item['count']
			
		
		cache.set(cache_key, result, 300)
		return result
		
	def update_reactions_cache(self):
		cache.delete(self.get_cache_key())
		return self.get_reactions_count()

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
	
class News(ReactionMixin, models.Model):
	title = models.CharField(max_length=255)
	content = models.TextField()
	published_date = models.DateTimeField(auto_now_add=True)
	category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, related_name='news')
	author = models.ForeignKey('app.User', on_delete=models.CASCADE, related_name='news_articles')
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	dislikes = models.IntegerField(default=0)
	image = models.ImageField(upload_to='news_images/', blank=True, null=True)
	attachment = models.FileField(upload_to='news_files/', blank=True, null=True)
	is_published = models.BooleanField(default=True, verbose_name="Опубликовано")

	def __str__(self):
		return self.title

class NewsComment(ReactionMixin, models.Model):
	news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
	author = models.ForeignKey('app.User', on_delete=models.CASCADE, related_name='news_comments')
	text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	likes = models.IntegerField(default=0)
	dislikes = models.IntegerField(default=0)

class EventAlbum(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    event_date = models.DateField(auto_now_add=True, verbose_name="Дата мероприятия")
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class EventPhoto(models.Model):
    album = models.ForeignKey(EventAlbum, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='event_photos/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('app.User', on_delete=models.CASCADE, related_name='event_photos')
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

class EventComment(ReactionMixin, models.Model):
    album = models.ForeignKey(EventAlbum, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('app.User', on_delete=models.CASCADE, related_name='event_comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

class KnowledgeComment(models.Model):
    article = models.ForeignKey(KnowledgeArticle, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('app.User', on_delete=models.CASCADE, related_name='knowledge_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
	

class Reaction(models.Model):
	LIKE = 'like'
	DISLIKE = 'dislike'
	REACTION_CHOICES = [
		(LIKE, 'Like'),
		(DISLIKE, 'Dislike'),
	]

	user = models.ForeignKey('app.User', on_delete=models.CASCADE)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ['user', 'content_type', 'object_id']
		indexes = [
			models.Index(fields=['content_type', 'object_id']),
		]

class PhotoComment(models.Model):
    photo = models.ForeignKey(EventPhoto, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)