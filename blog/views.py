from django.shortcuts import render
from django.db.models import Q
from .models import Article, Category

class SerachView(ListView):
    model = City
    template_name = 'serach_result.html'

    def get_queryset(self):
        query = self.request.GET.get('q', False)
        if query:

          article_list = Article.objects.filter(
              Q(title__icontains=query) | Q(content__icontains=query)
          )
          category_list = Category.objects.filter(
              Q(name__icontains=query)
          )
        else:
           article_query = Article.objects.all()
           category_query = Category.objects.all()
           object_list = article_query + category_query

        return object_list
