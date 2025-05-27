from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.models import KnowledgeArticle
from .forms import ArticleForm

def article_list(request):
    articles = KnowledgeArticle.objects.all().order_by('-published_at')
    return render(request, 'kb/article_list.html', {'articles': articles})

def article_detail(request, pk):
    article = get_object_or_404(KnowledgeArticle, pk=pk)
    return render(request, 'kb/article_detail.html', {'article': article})

@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, 'Статья успешно создана!')
            return redirect('kb:kb_detail', pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'kb/article_form.html', {'form': form})

@login_required
def article_edit(request, pk):
    article = get_object_or_404(KnowledgeArticle, pk=pk)
    if request.user != article.author:
        messages.error(request, 'У вас нет прав для редактирования этой статьи!')
        return redirect('kb:kb_detail', pk=article.pk)
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статья успешно обновлена!')
            return redirect('kb:kb_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'kb/article_form.html', {'form': form})

@login_required
def article_delete(request, pk):
    article = get_object_or_404(KnowledgeArticle, pk=pk)
    if request.user != article.author:
        messages.error(request, 'У вас нет прав для удаления этой статьи!')
        return redirect('kb:kb_detail', pk=article.pk)
    
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Статья успешно удалена!')
        return redirect('kb:kb_list')
    return render(request, 'kb/article_confirm_delete.html', {'article': article})
