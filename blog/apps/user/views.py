from django.views.generic import CreateView, TemplateView
from apps.user.forms import RegisterForm, LoginForm, PerfilForm
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView as LoginViewDjango
from django.contrib.auth.views import LogoutView as LogoutViewDjango 
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from apps.post.models import Post  # Importacion del modelo post para el perfil del usuario

class IndexView(TemplateView):
    template_name = 'index.html'  # Nombre de la plantilla a renderizar
    def get_context_data(self, **kwargs): # Método para obtener el contexto de la vista
        context = super().get_context_data(**kwargs) # Obtiene el contexto de la plantilla
        context['posts'] = Post.objects.all().order_by('-created_at')[:5] # Obtiene los últimos 5 posts
        return context  # Retorna el contexto actualizado
    
#class UserProfileView(TemplateView):      # Vista para el perfil del usuario
class UserProfileView(LoginRequiredMixin, TemplateView):      # Vista para el perfil del usuario 
    template_name = 'user/user_profile.html'      # Nombre de la plantilla a renderizar

    def get_context_data(self, **kwargs):      # Método para obtener el contexto de la vista
        context = super().get_context_data(**kwargs)
        form = PerfilForm(instance=self.request.user)      # Crea una instancia del formulario con los datos del usuario actual
        context['form'] = form      # Agrega el formulario al contexto
        return context
    
    def post(self, request): # Manejo del formulario de edición del perfil
        form = PerfilForm(request.POST, request.FILES, instance=request.user) # Crea una instancia del formulario con los datos del usuario actual
        if form.is_valid(): # Verifica si el formulario es válido
            form.save() # Guarda los cambios en el perfil del usuario
            return redirect('user:user_profile') # Redirige al perfil del usuario después de guardar los cambios
        return render(request, 'user/user_profile.html', {'form': form}) # Renderiza la plantilla con el formulario si no es válido

class RegisterView(CreateView):      # Vista para el registro de usuarios
    template_name = 'auth/auth_register.html'      # Nombre de la plantilla a renderizar
    form_class = RegisterForm      # Clase del formulario a utilizar
    success_url = reverse_lazy('home')   # URL a redirigir después de un registro exitoso

    def form_valid(self, form):   # Método para manejar el formulario válido
        response = super().form_valid(form)  # Llama al método form_valid de la clase padre

        registered_group = Group.objects.get(name='Registered')  # Obtiene el grupo de usuarios registrados
        self.object.groups.add(registered_group)  # Agrega el usuario al grupo de registrados
        print("FILES:", self.request.FILES)  # Imprime los archivos subidos para depuración
        return response  # Retorna la respuesta del formulario válido
    
class LoginView(LoginViewDjango):  # Vista para el inicio de sesión
    template_name = 'auth/auth_login.html'  # Nombre de la plantilla a renderizar
    authentication_form = LoginForm  # Clase del formulario de autenticación a utilizar

    def get_success_url(self):  # Método para obtener la URL de éxito después de un inicio de sesión exitoso
        return reverse_lazy('home')  # Redirige al usuario a la página principal después de un inicio de sesión exitoso

class LogoutView(LogoutViewDjango):
    next_page = reverse_lazy('home')  # URL a redirigir después de un cierre de sesión exitoso
