from django.urls import path
from . import views
from app.urls import BaseURLPatterns

app_name = 'kb'

urlpatterns = BaseURLPatterns(views, 'kb').get_urlpatterns()

urlpatterns.append(path('<int:pk>/edit/', views.article_edit, name='kb_edit'))
urlpatterns.append(path('<int:pk>/delete/', views.article_delete, name='kb_delete')) 