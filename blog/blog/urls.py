"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from apps.user.views import IndexView  

urlpatterns = [
    path('admin/', admin.site.urls), # URL para el panel de administración
    path('', IndexView.as_view(), name='home'), # URL para la página de inicio
    path('user/', include('apps.user.urls')), # URLs de la aplicación de usuario
    path('posts/', include('apps.post.urls')), # URLs de la aplicación de posts
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Servir archivos estáticos en modo DEBUG

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Servir archivos multimedia en modo DEBUG    
