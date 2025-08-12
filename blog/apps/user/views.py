from django.shortcuts import redirect, render
from django.contrib.auth.views import PasswordResetView as DjangoPasswordResetView
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from apps.post.models import Post
from apps.user.forms import PerfilForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import CustomUserCreationForm, AvatarUpdateForm
from django.contrib.auth import login, logout
from .models import User


    
class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        context['posts'] = user.posts.all().order_by('-created_at')
        if 'form' not in context:
            context['form'] = PerfilForm(instance=user)
        return context

    def post(self, request, *args, **kwargs):
        form = PerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('user:user_profile')
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
    

class RegisterView(CreateView):      # Vista para el registro de usuarios
    template_name = 'auth/auth_register.html'      # Nombre de la plantilla a renderizar
    form_class = CustomUserCreationForm      # Clase del formulario a utilizar
    success_url = reverse_lazy('user:auth_login')   # URL a redirigir después de un registro exitoso

    def form_valid(self, form):
        print("Ejecutando form_valid")
        response = super().form_valid(form)
        registered_group, created = Group.objects.get_or_create(name='Registered')
        self.object.groups.add(registered_group)
        print(f"Grupo asignado: {registered_group.name}, creado: {created}")
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
    
class UserLoginView(FormView):
    template_name = 'auth/auth_login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('user:user_profile')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user:user_profile')
        return super().dispatch(request, *args, **kwargs)  # Redirige al usuario a la página principal después de un inicio de sesión exitoso

class UserLogoutView(RedirectView):
    template_name = 'auth/auth_login.html'
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('user:auth_login')
    

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