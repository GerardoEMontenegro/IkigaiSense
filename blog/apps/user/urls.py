from django.urls import path
from django.contrib.auth import views as auth_views    
from apps.user import views as views

app_name = 'user'

urlpatterns = [
    path('user/profile/', views.UserProfileView.as_view(), name='user_profile'),    # Ruta para el perfil del usuario
    path('auth/register/', views.RegisterView.as_view(), name='auth_register'),    # Ruta para el registro de usuario
    path('auth/login/', views.LoginView.as_view(), name='auth_login'),    # Ruta para el inicio de sesión del usuario
    path('auth/logout/', views.LogoutView.as_view(), name='auth_logout'),    # Ruta para el cierre de sesión del usuario
    path('user/update-avatar/', views.AvatarUpdateView.as_view(), name='update_avatar'),
    path('reset/password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(
            template_name='ps_reset/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
            template_name='ps_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='ps_reset/password_reset_complete.html'),        
         name='password_reset_complete'),
    ]