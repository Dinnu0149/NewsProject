from rest_framework import generics, status, pagination, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TagSerializer, NewsSerializer, LikeSerializer
from .models import Tag, News, Like
from rest_framework.parsers import MultiPartParser, FormParser


class NewsCreateAPIView(generics.CreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    # permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "News created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsDeleteAPIView(generics.DestroyAPIView):
    queryset = News.objects.all()
    # permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "News deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class NewsPagination(pagination.PageNumberPagination):
    page_size = 3  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100
    ordering = ('-created_at',)


class NewsListAPIView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    pagination_class = NewsPagination


class TagView(generics.ListAPIView):
    queryset = Tag.objects.all().order_by('-name')
    serializer_class = TagSerializer


class NewsByTagAPIView(generics.ListAPIView):
    serializer_class = NewsSerializer
    pagination_class = NewsPagination

    def get_queryset(self):
        tag_id = self.kwargs['tag_id']
        return News.objects.filter(tags__id=tag_id)


class NewsDetailAPIView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increment_views()  # Increment views
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class LikeNewsAPIView(APIView):
    def post(self, request, news_id):
        news = News.objects.get(pk=news_id)
        unique_user_id = request.unique_user_id

        action = request.data.get('action')
        like, created = Like.objects.get_or_create(session_key=unique_user_id, news=news)
        like.handle_liking(action)

        likes_count = news.likes.filter(liked=True).count()
        dislikes_count = news.likes.filter(liked=False).count()

        response = {
            'likes_count': likes_count,
            'dislikes_count': dislikes_count,
            'user_liked': like.liked,
        }
        return Response(response, status=status.HTTP_200_OK)


class NewsStatisticsAPIView(APIView):
    def get(self, request):
        news_stats = News.objects.values('pk', 'title', 'views').order_by('-views')
        return Response(news_stats)
