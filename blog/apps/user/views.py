from django.contrib.auth.views import PasswordResetView as DjangoPasswordResetView
from django.views.generic import CreateView, TemplateView, RedirectView
from apps.user.forms import LoginForm, PerfilForm
from .forms import CustomUserCreationForm, AvatarUpdateForm
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView as LoginViewDjango, LogoutView as LogoutViewDjango 
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from apps.post.models import Post  # Importacion del modelo post para el perfil del usuario
from .models import User  # Importacion del modelo User para el perfil del usuario
from django.contrib.auth import login, logout

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
    form_class = CustomUserCreationForm      # Clase del formulario a utilizar
    success_url = reverse_lazy('user:auth_login')   # URL a redirigir después de un registro exitoso

    def form_valid(self, form):
        response = super().form_valid(form)
        registered_group = Group.objects.get(name='Registered')  # Asegúrate que el grupo exista
        self.object.groups.add(registered_group)  # Aquí se corrige el método
        return response
        

    def get_form(self, form_class=None):
        """
        Sobrescribimos get_form para pasar request.FILES al formulario (para avatar)
        """
        form_class = self.get_form_class()
        return form_class(self.request.POST or None, self.request.FILES or None)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user:user_profile')
        return super().dispatch(request, *args, **kwargs)
    
class LoginView(LoginViewDjango):  # Vista para el inicio de sesión
    template_name = 'auth/auth_login.html'  # Nombre de la plantilla a renderizar
    authentication_form = LoginForm  # Clase del formulario de autenticación a utilizar

    def get_success_url(self):  # Método para obtener la URL de éxito después de un inicio de sesión exitoso
        return reverse_lazy('home')  # Redirige al usuario a la página principal después de un inicio de sesión exitoso

class LogoutView(RedirectView):
    template_name = 'home'
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')
       
class AvatarUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = AvatarUpdateForm
    template_name = 'user/update_avatar.html'
    success_url = reverse_lazy('user:user_profile')  # Ajustá según el nombre real de tu URL de perfil

    def get_object(self):
        return self.request.user
    

    
class PasswordResetView(DjangoPasswordResetView):
    template_name = 'ps_reset/password_reset_form.html'
    email_template_name = 'ps_reset/password_reset_email.html'
    subject_template_name = 'ps_reset/password_reset_subject.txt'
    success_url = reverse_lazy('user:password_reset_done')

    def get_email_context(self):
        context = super().get_email_context()
        context['domain'] = '127.0.0.1:3000'  # Cambia por tu frontend
        context['protocol'] = 'http'
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cambiar contraseña'
        return context