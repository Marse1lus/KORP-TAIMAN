from django.urls import path
from . import views
from app.urls import BaseURLPatterns

app_name = 'news'

urlpatterns = BaseURLPatterns(views, 'news').get_urlpatterns() 