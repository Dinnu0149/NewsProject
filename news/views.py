from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.core.paginator import Paginator
from django.core import serializers
from django.http import JsonResponse
from django.contrib import messages
from .models import *
import json


def news_list(request):
    """Initial load of news items, handle paginator to get 3 items
     and new request for infinite scrolling"""
    page = request.GET.get('page', 1)
    news = News.objects.all()
    paginator = Paginator(news, 2)
    news_page = paginator.page(page)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        news_data = serializers.serialize('json', news_page)

        response = {
            'news': news_data,
            'has_next': news_page.has_next()
        }
        return JsonResponse(response, safe=False)

    context = {
        'news': news_page
    }
    return render(request, 'news/news_list.html', context)


def news_detail(request, pk):
    """Display news item and increment views"""
    news = get_object_or_404(News, pk=pk)
    news.increment_views()

    context = {
        'news': news
    }
    return render(request, 'news/news_detail.html', context)


def news_by_tag(request, tag_id):
    """Filter news by tags"""
    tag = get_object_or_404(Tag, pk=tag_id)
    news = News.objects.filter(tags__pk=tag_id)

    context = {
        'news': news,
        'tag': tag
    }
    return render(request, 'news/news_by_tag.html', context)


def like_news(request, news_id):
    """Using user session to handle liking functionality"""
    news = get_object_or_404(News, pk=news_id)
    session_key = request.session.session_key
    user_liked = None

    if not session_key:
        request.session.save()
        session_key = request.session.session_key

    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')  # 'like' or 'dislike'

        like, created = Like.objects.get_or_create(session_key=session_key, news=news)
        like.handle_liking(action)
        user_liked = like.liked
        print(user_liked)

    likes_count = news.likes.filter(liked=True).count()
    dislikes_count = news.likes.filter(liked=False).count()

    response = {
        'likes_count': likes_count,
        'dislikes_count': dislikes_count,
        'user_liked': user_liked,
    }
    return JsonResponse(response)


def news_statistics(request):
    """Getting statistics for all news"""
    news = News.objects.values('pk', 'title', 'views').order_by('-views')

    context = {
        'news': news,
    }
    return render(request, 'news/statistics.html', context)
