from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.core.paginator import Paginator
from django.core import serializers
from django.http import JsonResponse
from django.contrib import messages
from .models import *
from .forms import NewsForm
import json


def create_news(request):
    """Creating news content"""
    form = NewsForm()
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'News created successfully', extra_tags='alert-success')
            return redirect('news:news_list')

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}', extra_tags='alert-danger')
            return redirect('news:create_news')

    context = {
        'form': form
    }
    return render(request, 'news/create_news.html', context)


def delete_news(request, pk):
    """Deleting news"""
    back = request.META.get('HTTP_REFERER', '/')
    try:
        news = get_object_or_404(News, pk=pk)
        news.delete()

        messages.success(request, 'News deleted successfully', extra_tags='bg-success')
        return redirect('news:news_list')

    except News.DoesNotExist:
        messages.success(request, 'Item does not exist', extra_tags='bg-danger')
        return HttpResponseRedirect(back)



def news_list(request):
    """Initial load of news items, handle paginator to get 3 items
     and new request for infinite scrolling"""
    page = request.GET.get('page', 1)
    news = News.objects.all()
    paginator = Paginator(news, 3)
    news_page = paginator.page(page)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        news_data = [item.serialize_format() for item in news_page]

        response = {
            'news': news_data,
            'has_next': news_page.has_next()
        }
        return JsonResponse(response, safe=False)

    context = {
        'news': news_page,
        'has_next': news_page.has_next(),

    }
    return render(request, 'news/news_list.html', context)


def news_by_tag(request, tag_id):
    """Initial load of tag news items, handle paginator to get 3 items
     and new request for infinite scrolling"""
    page = request.GET.get('page', 1)
    news = News.objects.filter(tags__pk=tag_id)
    tag = get_object_or_404(Tag, pk=tag_id)

    paginator = Paginator(news, 3)
    news_page = paginator.page(page)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        news_data = [item.serialize_format() for item in news_page]

        response = {
            'news': news_data,
            'has_next': news_page.has_next()
        }
        return JsonResponse(response, safe=False)

    context = {
        'news': news_page,
        'has_next': news_page.has_next(),
        'tag': tag
    }
    return render(request, 'news/news_by_tag.html', context)


def news_detail(request, pk):
    """Display news item and adding increment +1 to views"""
    news = get_object_or_404(News, pk=pk)
    tags = Tag.objects.all()
    news.increment_views()

    context = {
        'news': news,
        'tags': tags,
    }
    return render(request, 'news/news_detail.html', context)


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
