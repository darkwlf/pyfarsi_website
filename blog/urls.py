from django.urls import path
from . import views


app_name = "blog"
urlpatterns = (
    path("articles/<int:page>/", views.Articles.as_view(), name="articles"),
    path(
        "articles/<int:pk>/<slug:slug>/",
        views.ArticleDetailView.as_view(),
        name="article_detail",
    ),
    path("comment/", views.CreateCommentView.as_view(), name="create_comment"),
    path("article/<int:pk>/", views.GetCommentsView.as_view(), name="get_comments"),
)
