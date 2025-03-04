from django.db.models import Q
from django.http import JsonResponse
from media.models import Media
from actual.models import Actual
from appeals.models import Appeal

def search(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'results': []})
    
    results = []
    
    # Поиск по медиа
    media_results = Media.objects.filter(
    ).values('id', 'header', 'summary')[:5]
    
    # Поиск по актуальному
    actual_results = Actual.objects.filter(
    ).values('id', 'header', 'summary')[:5]
    
    # Поиск по обращениям
    appeals_results = Appeal.objects.filter(
    ).values('id', 'title', 'text')[:5]
    
    
    for item in media_results:
        results.append({
            'type': 'media',
            'id': item['id'],
            'header': item['header'],
            'summary': item['summary'][:200] + '...' 
        })
    
    for item in actual_results:
        results.append({
            'type': 'actual',
            'id': item['id'],
            'header': item['header'][:200] + '...',
            'summary': item['summary'] 
        })
    
    for item in appeals_results:
        results.append({
            'type': 'appeals',
            'id': item['id'],
            'title': item['title'][:200] + '...',
            'text': item['text'][:100] + '...' 
        })
    
    return JsonResponse({'results': results}) 