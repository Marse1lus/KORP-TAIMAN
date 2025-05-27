from django.contrib import admin
from .models import User, NewsCategory, EventAlbum, EventPhoto, EventComment, KnowledgeCategory, KnowledgeArticle, KnowledgeComment
from albums.models import PhotoComment


admin.site.register(User)
admin.site.register(NewsCategory)
# admin.site.register(News)
# admin.site.register(NewsComment)

class EventAlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'author')
    fields = ('title', 'description', 'event_date', 'author', 'likes', 'dislikes')

admin.site.register(EventAlbum, EventAlbumAdmin)
admin.site.register(EventPhoto)
admin.site.register(EventComment)
admin.site.register(KnowledgeCategory)
admin.site.register(KnowledgeArticle)
admin.site.register(KnowledgeComment)
admin.site.register(PhotoComment)
