from django.db.models import Q
from .models import Article
from django.views.generic import ListView


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
