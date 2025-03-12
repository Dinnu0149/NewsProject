from django.contrib import admin
from .models import *


@admin.register(News)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', )


@admin.register(Tag)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', )
