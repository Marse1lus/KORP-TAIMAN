from django.contrib import admin
from .models import User, NewsCategory, News, NewsComment, EventAlbum, EventPhoto, EventComment, KnowledgeCategory, KnowledgeArticle, KnowledgeComment


admin.site.register(User)
admin.site.register(NewsCategory)
admin.site.register(News)
admin.site.register(NewsComment)
admin.site.register(EventAlbum)
admin.site.register(EventPhoto)
admin.site.register(EventComment)
admin.site.register(KnowledgeCategory)
admin.site.register(KnowledgeArticle)
admin.site.register(KnowledgeComment)
