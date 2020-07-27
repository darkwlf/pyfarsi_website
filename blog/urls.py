from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = (
    path('articles/<int:page>/', views.Articles.as_view(), name='articles'),
    path('article/<int:pk>/<slug:slug>/', views.ArticleDetail.as_view(), name='article_detail'),
    path('comment/', views.CreateComments.as_view(), name='create_comment'),
    path('comments/<int:pk>/', views.GetComments.as_view(), name='get_comments')
)
