from django.urls import path
from django.contrib.auth import views as auth_views    
from apps.user import views as views

app_name = 'user'

urlpatterns = [
    path('user/profile/', views.UserProfileView.as_view(), name='user_profile'),    
    path('auth/register/', views.RegisterView.as_view(), name='auth_register'),    
    path('auth/login/', views.UserLoginView.as_view(), name='auth_login'),    
    path('auth/logout/', views.UserLogoutView.as_view(), name='auth_logout'),    
    path('user/update-avatar/', views.AvatarUpdateView.as_view(), name='update_avatar'),
    path('reset/password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(
            template_name='ps_reset/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
            template_name='ps_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='ps_reset/password_reset_complete.html'),        
         name='password_reset_complete'),
    ]