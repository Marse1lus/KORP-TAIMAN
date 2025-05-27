from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import News
from .forms import NewsForm, NewsCommentForm

def news_list(request):
    news = News.objects.all().order_by('-published_date')
    return render(request, 'news_app/news_list.html', {'news': news})

def news_detail(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    comments = news_item.comments.select_related('author').all()
    if request.method == 'POST' and request.user.is_authenticated:
        form = NewsCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news_item
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('news:news_detail', pk=pk)
    else:
        form = NewsCommentForm()
    return render(request, 'news_app/news_detail.html', {
        'news_item': news_item,
        'comments': comments,
        'form': form
    })

@login_required
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(request, 'Новость успешно создана!')
            return redirect('news:news_detail', pk=news.pk)
    else:
        form = NewsForm()
    return render(request, 'news_app/news_form.html', {'form': form})

@login_required
def news_edit(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.user != news.author:
        messages.error(request, 'У вас нет прав для редактирования этой новости!')
        return redirect('news:news_detail', pk=news.pk)
    
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'Новость успешно обновлена!')
            return redirect('news:news_detail', pk=news.pk)
    else:
        form = NewsForm(instance=news)
    return render(request, 'news_app/news_form.html', {'form': form})

@login_required
def news_delete(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.user != news.author:
        messages.error(request, 'У вас нет прав для удаления этой новости!')
        return redirect('news:news_detail', pk=news.pk)
    
    if request.method == 'POST':
        news.delete()
        messages.success(request, 'Новость успешно удалена!')
        return redirect('news:news_list')
    return render(request, 'news_app/news_confirm_delete.html', {'news': news})
