from __future__ import absolute_import, unicode_literals
from celery import shared_task
from newsapi import NewsApiClient
from django.conf import settings
from django.utils import timezone, dateformat
from datetime import timedelta
import math
from .models import Article, Source,Company
import json
from .scraper.article_scraper import extract_news_content


@shared_task(name='Get Latest News')
def get_latest_news():

    newsapi = NewsApiClient(api_key=settings.NEWS_API_KEY)

    from_date = dateformat.format(timezone.now() - timedelta(days=1), 'Y-m-d')
    to_date = dateformat.format(timezone.now(), 'Y-m-d')

    new_articles_count = 0
    total = 0

    companies = Company.objects.filter(status='active')


    for comp in companies :

        sources = ",".join([p.slug for p in comp.sources.all()])

        articles = []
        page_number = 1

        try :
            while True:
                all_articles = newsapi.get_everything(q=comp.query,
                                                    sources=sources,
                                                    from_param=from_date,
                                                    to=to_date,
                                                    language='en',
                                                    sort_by='relevancy',
                                                    page=page_number)
                articles.extend(all_articles['articles'])
                if math.ceil(all_articles['totalResults'] / 20 > page_number):
                    page_number += 1
                else:
                    break


            
            for article in articles:
                source = Source.objects.filter(slug=article['source']['id']).first()
                if Article.objects.filter(url=article['url']).count() == 0:
                    art = Article(title=article['title'], url=article['url'], published_at=article['publishedAt'], source=source,company=comp)
                    art.save()
                    new_articles_count += 1
            
            total += len(articles)
        except :
            continue

    return {'new': new_articles_count, 'total': total}


@shared_task(name='Scrape News Content')
def extract_features():

    articles = Article.objects.filter(status="incomplete")

    successed = 0
    failed = 0
    for article in articles :
        res = extract_news_content(article.id)
        if res == True :
            successed += 1
        else : 
            failed += 1

    return {
        'result' :
            {
                'successed' : successed,
                'failed' : failed
            }
    }