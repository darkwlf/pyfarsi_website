from django.http import HttpRequest
from blog.models import Article


def check_author_or_superuser(request: HttpRequest, obj: Article):
    return request.user.is_superuser or not obj or obj.author == request.user
