from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from albums.forms import EventAlbumForm
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.core.cache import cache
from django.views.decorators.http import require_POST
from .models import EventAlbum, EventPhoto, EventComment, PhotoComment
from .forms import EventAlbumForm, EventPhotoForm, PhotoCommentForm, EventCommentForm



class EventAlbumList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        albums = EventAlbum.objects.all()
        serializer = EventAlbumSerializer(albums, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventAlbumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventPhotoList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        photos = EventPhoto.objects.all()
        album_id = request.query_params.get('album')
        if album_id:
            photos = photos.filter(album_id=album_id)
        serializer = EventPhotoSerializer(photos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventPhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventCommentList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        album_id = request.query_params.get('album')
        comments = EventComment.objects.filter(album_id=album_id)
        serializer = EventCommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def event_albums_list(request):
    albums = EventAlbum.objects.all().order_by('-event_date')
    return render(request, 'albums/event_albums_list.html', {'albums': albums})

def event_album_detail(request, pk):
    album = get_object_or_404(EventAlbum, pk=pk)
    comments = EventComment.objects.filter(album=album)
    album_type_id = ContentType.objects.get_for_model(EventAlbum).id
    photo_type_id = ContentType.objects.get_for_model(EventPhoto).id
    comment_type_id = ContentType.objects.get_for_model(EventComment).id

    if request.method == 'POST' and request.user.is_authenticated:
        form = EventCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.album = album
            comment.author = request.user
            comment.save()
            return redirect('event_album_detail', pk=pk)
    else:
        form = EventCommentForm()

    return render(request, 'ums/event_album_detail.html', {
        'album': album,
        'comments': comments,
        'form': form,
        'album_type_id': album_type_id,
        'photo_type_id': photo_type_id,
        'comment_type_id': comment_type_id,
    })

@login_required
def create_event_album(request):
    if request.method == 'POST':
        form = EventAlbumForm(request.POST)
        if form.is_valid():
            album = form.save()
            return redirect('event_album_detail', pk=album.pk)
    else:
        form = EventAlbumForm()
    return render(request, 'albums/create_event_album.html', {'form': form})

@login_required
def add_event_photo(request, pk):
    album = get_object_or_404(EventAlbum, pk=pk)
    if request.method == 'POST':
        files = request.FILES.getlist('photo')
        for f in files:
            EventPhoto.objects.create(album=album, author=request.user, photo=f)
        return redirect('event_album_detail', pk=album.pk)
    else:
        form = EventPhotoForm()
    return render(request, 'albums/add_event_photo.html', {'form': form, 'album': album})

@login_required
def add_event_comment(request, pk):
    album = get_object_or_404(EventAlbum, pk=pk)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            EventComment.objects.create(album=album, author=request.user, text=text)
            return redirect('event_album_detail', pk=album.pk)
    return render(request, 'albums/add_event_comment.html', {'album': album})

@login_required
def add_photo_comment(request, photo_id):
    photo = get_object_or_404(EventPhoto, pk=photo_id)
    if request.method == 'POST':
        form = PhotoCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.photo = photo
            comment.author = request.user
            comment.save()
            return redirect('event_album_detail', pk=photo.album.pk)
    else:
        form = PhotoCommentForm()
    return render(request, 'albums/add_photo_comment.html', {'form': form, 'photo': photo})

@login_required
def like_album(request, pk):
    album = get_object_or_404(EventAlbum, pk=pk)
    album.likes += 1
    album.save()
    return redirect('event_album_detail', pk=pk)

@login_required
def dislike_album(request, pk):
    album = get_object_or_404(EventAlbum, pk=pk)
    album.dislikes += 1
    album.save()
    return redirect('event_album_detail', pk=pk)

@login_required
def edit_event_album(request, pk):
    album = get_object_or_404(EventAlbum, pk=pk)
    if request.user != getattr(album, 'author', request.user):
        messages.error(request, 'У вас нет прав для редактирования этого альбома!')
        return redirect('event_album_detail', pk=album.pk)
    if request.method == 'POST':
        form = EventAlbumForm(request.POST, instance=album)
        if form.is_valid():
            form.save()
            messages.success(request, 'Альбом успешно обновлён!')
            return redirect('event_album_detail', pk=album.pk)
    else:
        form = EventAlbumForm(instance=album)
    return render(request, 'albums/edit_event_album.html', {'form': form, 'album': album})

@login_required
def delete_event_album(request, pk):
    album = get_object_or_404(EventAlbum, pk=pk)
    if request.user != getattr(album, 'author', request.user):
        messages.error(request, 'У вас нет прав для удаления этого альбома!')
        return redirect('event_album_detail', pk=album.pk)
    if request.method == 'POST':
        album.delete()
        messages.success(request, 'Альбом успешно удалён!')
        return redirect('event_albums_list')
    return render(request, 'albums/delete_event_album.html', {'album': album})

@login_required
def edit_event_comment(request, pk):
    comment = get_object_or_404(EventComment, pk=pk)
    if request.user != comment.author:
        return HttpResponseForbidden("Вы не можете редактировать этот комментарий.")
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            comment.text = text
            comment.save()
            return redirect('event_album_detail', pk=comment.album.pk)
    return render(request, 'albums/edit_event_comment.html', {'comment': comment})

@login_required
def delete_event_comment(request, album_id, pk):
    comment = get_object_or_404(EventComment, pk=pk, album_id=album_id)
    if request.user != comment.author:
        return HttpResponseForbidden("Вы не можете удалить этот комментарий.")
    if request.method == 'POST':
        comment.delete()
        return redirect('event_album_detail', pk=album_id)
    return render(request, 'albums/delete_event_comment.html', {'comment': comment})

@login_required
def like_event_photo(request, pk):
    photo = get_object_or_404(EventPhoto, pk=pk)
    if not hasattr(photo, 'likes'):
        photo.likes = 0
    photo.likes += 1
    photo.save()
    return JsonResponse({'likes': photo.likes})

@login_required
def dislike_event_photo(request, pk):
    photo = get_object_or_404(EventPhoto, pk=pk)
    if not hasattr(photo, 'dislikes'):
        photo.dislikes = 0
    photo.dislikes += 1
    photo.save()
    return JsonResponse({'dislikes': photo.dislikes})
