from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_albums_list, name='event_albums_list'),
    path('<int:pk>/', views.event_album_detail, name='event_album_detail'),
    path('create/', views.create_event_album, name='create_event_album'),
    path('<int:pk>/add_photo/', views.add_event_photo, name='add_event_photo'),
    path('<int:pk>/add_comment/', views.add_event_comment, name='add_event_comment'),
    path('photo/<int:photo_id>/add_comment/', views.add_photo_comment, name='add_photo_comment'),
    path('<int:pk>/like/', views.like_album, name='like_album'),
    path('<int:pk>/dislike/', views.dislike_album, name='dislike_album'),
    path('<int:pk>/edit/', views.edit_event_album, name='edit_event_album'),
    path('<int:pk>/delete/', views.delete_event_album, name='delete_event_album'),
    path('comment/<int:pk>/edit/', views.edit_event_comment, name='edit_event_comment'),
    path('<int:album_id>/comment/<int:pk>/delete/', views.delete_event_comment, name='delete_event_comment'),
    path('photo/<int:pk>/like/', views.like_event_photo, name='like_event_photo'),
    path('photo/<int:pk>/dislike/', views.dislike_event_photo, name='dislike_event_photo'),
] 