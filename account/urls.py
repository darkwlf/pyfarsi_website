from django.urls import path
from . import views
app_name = 'account'
urlpatterns = (
    path('login/', views.Login.as_view(), nane='login'),
    path('register/', views.Register.as_view(), name='register')
)
