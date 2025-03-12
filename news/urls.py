from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'news'

urlpatterns = [
                  path('', views.news_list, name='news_list'),
                  path('<int:pk>/', views.news_detail, name='news_detail'),
                  path('tag/<int:tag_id>/', views.news_by_tag, name='news_by_tag'),
                  path('like/<int:news_id>/', views.like_news, name='like_news'),
                  path('statistics/', views.news_statistics, name='news_statistics'),
                  path('create/', views.create_news, name='create_news'),
                  path('delete/<int:pk>/', views.delete_news, name='delete_news'),

              ] + static(settings.STATIC_URL,
                         document_root=settings.STATIC_ROOT)
