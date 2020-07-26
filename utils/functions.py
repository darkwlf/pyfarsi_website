from django.http import HttpRequest
from blog.models import Article


def check_self_article_or_supper_user(request: HttpRequest, obj: Article):
    return request.user.is_superuser or not obj or obj.author == request.user
