from django.db import models
from django.conf import settings
from app.models import NewsCategory

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='news_app_articles')
    published_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    attachment = models.FileField(upload_to='news_files/', blank=True, null=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, related_name='news_app_news', blank=True, null=True, verbose_name='Категория')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    likes = models.IntegerField(default=0, verbose_name='Лайки')
    dislikes = models.IntegerField(default=0, verbose_name='Дизлайки')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-published_date']

    def __str__(self):
        return self.title

class NewsComment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='news_app_comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Комментарий к новости'
        verbose_name_plural = 'Комментарии к новостям'
        ordering = ['-created_at']

    def __str__(self):
        return f'Комментарий от {self.author} к новости {self.news}'
