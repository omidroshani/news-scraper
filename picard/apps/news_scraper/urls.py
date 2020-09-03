from django.urls import path
from .views import update_sources,get_latest_news,get_feature_extraction


urlpatterns = [
    path('sources', update_sources, name='sources'),
    path('latest-news', get_latest_news, name='get_latest_news'),
    path('feature', get_feature_extraction, name='get_feature_extraction'),
    # path('hello', update_sources_2, name='extract_news_content'),
]