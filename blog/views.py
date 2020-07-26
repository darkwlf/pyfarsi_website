from django.shortcuts import render
from django.db.models import Q
from .models import Article
from django.views.generic import ListView


class Article(ListView):
    model = Article
    template_name = 'article.html'
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
