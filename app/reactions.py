from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.cache import cache

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
            count=models.Count('id')
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