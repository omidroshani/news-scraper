from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from newsapi import NewsApiClient
from django.conf import settings
from .models import Source,Article
from .tasks import get_latest_news as gln
from .tasks import extract_features as ef
from django.utils import timezone, dateformat
from .scraper.article_scraper import extract_news_content
from django.core.paginator import Paginator
from .serializers import ArticleSerializer

@api_view(['GET'])
def update_sources(request):
    newsapi = NewsApiClient(api_key=settings.NEWS_API_KEY)
    sources = newsapi.get_sources()
    for src in sources['sources']:
        current_src = Source.objects.filter(slug=src['id'])
        if current_src.count() > 0:
            current_src.update(title=src['name'], description=src['description'], url=src['url'], language=src['language'], category=src['category'])
        else:
            new_src = Source(title=src['name'], slug=src['id'], description=src['description'], url=src['url'], language=src['language'], category=src['category'])
            new_src.save()
    return Response({'results': sources})


@api_view(['POST'])
def get_latest_news(request):
    response = gln.delay()
    return Response({'task': {
        'id': response.id,
        'started_at': timezone.now()
    }})

@api_view(['POST'])
def get_feature_extraction(request):
    response = ef.delay()
    return Response({'task': {
        'id': response.id,
        'started_at': timezone.now()
    }})

@api_view(['GET'])
def get_all_articles(request):
    article_list = Article.objects.all()
    paginator = Paginator(article_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return Response(ArticleSerializer(page_obj, many=True).data)
