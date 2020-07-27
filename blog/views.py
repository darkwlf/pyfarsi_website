from django.db.models import Q
from .models import Article, Comment
from .serializers import CreateCommentSerializer
from django.views.generic import ListView
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


class CreateCommentView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CreateCommentSerializer
