from app.models import KnowledgeCategory

def categories_processor(request):
    return {
        'categories': KnowledgeCategory.objects.all()
    }