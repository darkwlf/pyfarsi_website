from rest_framework.pagination import PageNumberPagination


class CommentPaginator(PageNumberPagination):
    page_size = 15
    page_query_param = 'page'
