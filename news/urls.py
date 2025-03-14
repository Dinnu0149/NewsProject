from django.urls import path
from .views import (
    NewsCreateAPIView,
    NewsDeleteAPIView,
    NewsListAPIView,
    NewsByTagAPIView,
    NewsDetailAPIView,
    LikeNewsAPIView,
    NewsStatisticsAPIView,
    TagView,
)

urlpatterns = [
    path('create/', NewsCreateAPIView.as_view(), name='news_create'),
    path('delete/<int:pk>/', NewsDeleteAPIView.as_view(), name='news_delete'),
    path('list/', NewsListAPIView.as_view(), name='news_list'),
    path('tag/<int:tag_id>/', NewsByTagAPIView.as_view(), name='news_by_tag'),
    path('tags/', TagView.as_view(), name='tags'),
    path('detail/<int:pk>/', NewsDetailAPIView.as_view(), name='news_detail'),
    path('like/<int:news_id>/', LikeNewsAPIView.as_view(), name='like_news'),
    path('statistics/', NewsStatisticsAPIView.as_view(), name='news_statistics'),
]
