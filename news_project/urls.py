from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('senior/admin/panel/', admin.site.urls),
    path('api/news/', include('news.urls')),
]
