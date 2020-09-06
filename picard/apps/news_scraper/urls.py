from django.urls import path
from .views import update_sources,get_latest_news,get_feature_extraction,get_all_articles


urlpatterns = [
    path('sources', update_sources, name='sources'),
    path('latest-news', get_latest_news, name='get_latest_news'),
    path('feature', get_feature_extraction, name='get_feature_extraction'),
    path('articles', get_all_articles, name='get_all_articles'),
    # path('hello', update_sources_2, name='extract_news_content'),
]