from django import forms
from albums.models import EventAlbum, EventPhoto, PhotoComment, EventComment

class EventAlbumForm(forms.ModelForm):
    class Meta:
        model = EventAlbum
        fields = ['title', 'description', 'event_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'event_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class EventPhotoForm(forms.ModelForm):
    class Meta:
        model = EventPhoto
        fields = ['photo', 'caption']
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'caption': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PhotoCommentForm(forms.ModelForm):
    class Meta:
        model = PhotoComment
        fields = ['text'] 
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class EventCommentForm(forms.ModelForm):
    class Meta:
        model = EventComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        } 