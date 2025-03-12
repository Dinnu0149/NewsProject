from typing import Dict, Any
from django.db import models
from django.db.models import TextField, CharField, PositiveIntegerField
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self) -> str:
        """this is used to get the detail url for news"""

        return reverse('news:news_by_tag',
                       args=[self.pk])


class News(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    picture = models.ImageField(upload_to='news_images/', blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self) -> str:
        """this is used to get the detail url for news"""

        return reverse('news:news_detail',
                       args=[self.pk])

    def serialize_format(self) -> dict:
        news_item = {
            'pk': self.pk,
            'fields': {
                'url': self.get_absolute_url(),
                'title': self.title,
                'text': self.text,
                'image': self.display_image(),
                'tags': [tag.name for tag in self.tags.all()],  # Include tag titles
                'total_likes': self.total_likes(),
                'total_dislikes': self.total_dislikes(),
                'views': self.views,
                'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
        }
        return news_item

    def increment_views(self) -> None:
        self.views += 1
        self.save()

    def total_likes(self) -> int:
        likes_count = self.likes.filter(liked=True).count()
        return likes_count

    def total_dislikes(self) -> int:
        dislikes_count = self.likes.filter(liked=False).count()
        return dislikes_count

    def display_image(self) -> str:
        image = self.picture.url if self.picture else ''
        return image


class Like(models.Model):
    session_key = models.CharField(max_length=40)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='likes')
    liked = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session_key', 'news')

    def __str__(self):
        return f"{'Liked' if self.liked else 'Disliked'} {self.news.title}"

    def handle_liking(self, action) -> bool:
        self.liked = True if action == 'like' else False
        self.save()

        return self.liked
