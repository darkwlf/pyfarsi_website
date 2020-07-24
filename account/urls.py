from django.urls import path
from . import views
app_name = 'account'
urlpatterns = (
    path('login/', views.Login.as_view(), nane='login'),
    path('register/', views.Register.as_view(), name='register'),
    path('reset/', views.UserPassReset.as_view(), name='reset_pass'),
    path('reset-done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('confirm-done/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('logout/', views.Logout.as_view(), name='logout')
)
