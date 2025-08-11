from django.views.generic import TemplateView
from apps.post.models import Post


class IndexView(TemplateView):
    template_name = 'index.html'  # Nombre de la plantilla a renderizar
    def get_context_data(self, **kwargs): # Método para obtener el contexto de la vista
        context = super().get_context_data(**kwargs) # Obtiene el contexto de la plantilla
        context['posts'] = Post.objects.all().order_by('-created_at')[:5] # Obtiene los últimos 5 posts
        return context  # Retorna el contexto actualizado