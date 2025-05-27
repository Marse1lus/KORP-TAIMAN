from rest_framework import serializers
from albums.models import EventAlbum, EventPhoto, EventComment, PhotoComment

class EventAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAlbum
        fields = ['id', 'title', 'description', 'event_date', 'likes', 'dislikes']

class EventPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPhoto
        fields = ['id', 'album', 'photo', 'caption', 'uploaded_at', 'author']

class EventCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventComment
        fields = ['id', 'album', 'author', 'text', 'created_at']

class PhotoCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoComment
        fields = ['id', 'photo', 'author', 'text', 'created_at'] 