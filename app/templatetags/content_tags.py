from django import template 
from django.utils.safestring import mark_safe

register = template.Library()

@register.inclusion_tag('app/tags/article_card.html')
def article_card(article):

	return{'article': article}

@register.inclusion_tag('app/tags/news_card.html')
def news_card(news):

	return{'news': news}

@register.inclusion_tag('app/tags/album_card.html')
def album_card(album):

	return{'album': album}

@register.inclusion_tag('app/tags/comment_card.html')
def comment_card(comment, user, comment_type_id, parent=None):

	context = {
		'comment': comment,
		'user': user,
		'can_edit': user == comment.author,
		'comment_type_id': comment_type_id
	}
	
	if hasattr(comment, 'article'):
		context['article'] = comment.article
		context['edit_url'] = 'edit_comment'
		context['delete_url'] = 'delete_comment'
	elif hasattr(comment, 'news'):
		context['news'] = comment.news
		context['edit_url'] = 'edit_news_comment'
		context['delete_url'] = 'delete_news_comment'
	elif hasattr(comment, 'album'):
		context['album'] = comment.album
		context['edit_url'] = 'edit_event_comment'
		context['delete_url'] = 'delete_event_comment'
	
	return context

@register.simple_tag
def format_date(date):

	return date.strftime("%d.%m.%Y %H:%M")
 