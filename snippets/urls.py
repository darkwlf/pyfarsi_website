from django.urls import path
from . import views
app_name = 'snippets'
urlpatterns = (
    path('group/<int:pk>/<slug:slug>/', views.Group.as_view(), name='group'),
    path('create-group/', views.CreateGroup.as_view(), name='create_group'),
    path('join-group-with-link/<str:invite_id>/', views.join_group, name='join_group_with_link'),
    path('create-snippet/<int:group_id>/', views.CreateSnippet.as_view(), name='create_snippet'),
    path('snippet/<int:pk>/', views.Snippet.as_view(), name='snippet'),
    path('join-group/<int:group_id>/', views.join_group, name='join_group'),
    path('close-snippet/<int:snippet_id>/', views.close_snippet, name='close_snippet')
)
