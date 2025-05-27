from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.cache import cache
from django.db.models import Count
from django.db import models
from app.reactions import ReactionMixin, Reaction

class EventAlbum(ReactionMixin, models.Model):
	title = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	event_date = models.DateField(verbose_name="Дата мероприятия")
	likes = models.IntegerField(default=0)
	dislikes = models.IntegerField(default=0)
	author = models.ForeignKey('app.User', on_delete=models.CASCADE, related_name='event_albums')

	def __str__(self):
		return self.title
	
class EventPhoto(models.Model):
	album = models.ForeignKey(EventAlbum, on_delete=models.CASCADE, related_name='photos')
	photo = models.ImageField(upload_to='event_photos/')
	caption = models.CharField(max_length=255, blank=True)
	uploaded_at = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey('app.User', on_delete=models.CASCADE, related_name='event_photos', null=True, blank=True)
	likes = models.IntegerField(default=0)
	dislikes = models.IntegerField(default=0)

	def __str__(self):
		return f"Фото для альбома {self.album.title}"

class EventComment(ReactionMixin, models.Model):
	album = models.ForeignKey(EventAlbum, on_delete=models.CASCADE, related_name='comments')
	author = models.ForeignKey('app.User', on_delete=models.CASCADE, related_name='albums_event_comments')
	text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	likes = models.IntegerField(default=0)
	dislikes = models.IntegerField(default=0)

class PhotoComment(models.Model):
	photo = models.ForeignKey(EventPhoto, on_delete=models.CASCADE, related_name='comments')
	author = models.ForeignKey('app.User', on_delete=models.CASCADE, related_name='albums_photo_comments')
	text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Комментарий от {self.author.username} к фото {self.photo.caption}"
