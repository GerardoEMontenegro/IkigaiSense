from django.urls import path
from apps.user import views as views

app_name = 'user'

urlpatterns = [
    path('user/profile/', views.UserProfileView.as_view(), name='user_profile'),    # Ruta para el perfil del usuario
    path('auth/register/', views.RegisterView.as_view(), name='auth_register'),    # Ruta para el registro de usuario
    path('auth/login/', views.LoginView.as_view(), name='auth_login'),    # Ruta para el inicio de sesión del usuario
    path('auth/logout/', views.LogoutView.as_view(), name='auth_logout'),    # Ruta para el cierre de sesión del usuario
    ]
