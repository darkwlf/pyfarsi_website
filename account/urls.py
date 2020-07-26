from django.urls import path
from . import views
app_name = 'account'
urlpatterns = (
    path('login/', views.Login.as_view(), name='login'),
    path('password-reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password-reset-done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('reset-confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset-complete/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('verify-email/<str:key>/', views.verify_email, name='verify_email'),
    path('register-complete/', views.register_complete, name='register_complete')
)
