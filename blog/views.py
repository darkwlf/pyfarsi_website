from django.db.models import Q
from .models import Article, Comment
from .serializers import CreateComment, GetComment
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from rest_framework.generics import CreateAPIView, ListAPIView
from utils import get_sub_category


class Articles(ListView):
    model = Article
    template_name = 'blog/articles.html'
    paginate_by = 9

    def get_queryset(self):
        if query := self.request.GET.get('q'):
            articles = Article.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        else:
            articles = Article.objects.all()
        if all_categories := self.request.GET.get('categories'):
            all_categories = [
                category for main_category in all_categories for category in get_sub_category(main_category)
            ]
            articles = articles.filter(categories__name__in=all_categories)
        return articles


class ArticleDetail(DetailView):
    model = Article
    template_name = 'blog/article.html'
    queryset = Article.objects.filter(status='p')


class CreateComments(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CreateComment


class GetComments(ListAPIView):
    serializer_class = GetComment

    def get_queryset(self):
        return Comment.objects.filter(article__id=self.kwargs['pk'])
