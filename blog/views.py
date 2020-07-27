from django.db.models import Q
from .models import Article, Comment
from .serializers import CreateCommentSerializer
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from rest_framework.generics import CreateAPIView


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


class ArticleDetailView(ListView):
    context_object_name = 'Article'
    template_name = 'blog/article_detail.html'
    model = Article


class CreateCommentView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CreateCommentSerializer
