from django.shortcuts import render
from django.db.models import Q
from .models import Article
from django.views.generic import ListView 


class ArticleView(ListView):
    model = Article
    template_name = 'article.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
          article_query = Article.objects.filter(
              Q(title__icontains=query) | Q(content__icontains=query)
          )     
                        
        else:
           article_query = Article.objects.all()

        return article_query
