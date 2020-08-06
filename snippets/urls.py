from django.urls import path
from . import views
app_name = 'snippets'
urlpatterns = (
    path('group/<int:pk>/<slug:slug>/', views.Group.as_view(), name='group'),
    path('create-group/', views.CreateGroup.as_view(), name='create_group'),
    path('join-group/<str:invite_id>/', views.join_group, name='join_group'),
    path('create-snippet/<int:group_id>/', views.CreateSnippet.as_view(), name='create_snippet'),
    path('snippet/<int:pk>/', views.Snippet.as_view(), name='snippet')
)
