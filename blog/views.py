from django.db.models import Q
from .models import Article, Comment
from .paginators import CommentPaginator
from .serializers import CreateComment, GetComment
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from rest_framework.generics import CreateAPIView, ListAPIView


class Articles(ListView):
    model = Article
    template_name = 'blog/articles.html'
    paginate_by = 9

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            article_query = Article.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        else:
            article_query = Article.objects.all()
        return article_query


class ArticleDetail(DetailView):
    model = Article
    template_name = "blog/article_detail.html"
    context_object_name = 'article'
    
    def get_queryset(self):
        query = Article.objects.filter(status='p')


class CreateCommentView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CreateComment


class GetCommentsView(ListAPIView):
    serializer_class = GetComment
    pagination_class = CommentPaginator

    def get_queryset(self):
        article_id = self.kwargs['pk']
        return Comment.objects.filter(id=article_id)
