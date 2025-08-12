from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordResetView as DjangoPasswordResetView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView
from django.views.generic.edit import FormView, CreateView, UpdateView

from apps.post.models import Post
from .forms import CustomUserCreationForm, AvatarUpdateForm
from .models import User


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        context['posts'] = user.posts.all().order_by('-created_at')
        return context

class RegisterView(CreateView):     
    template_name = 'auth/auth_register.html'      
    form_class = CustomUserCreationForm     
    success_url = reverse_lazy('user:auth_login')   

    def form_valid(self, form):
        print("Ejecutando form_valid")
        response = super().form_valid(form)
        registered_group, created = Group.objects.get_or_create(name='Registered')
        self.object.groups.add(registered_group)
        print(f"Grupo asignado: {registered_group.name}, creado: {created}")
        return response


    def get_form(self, form_class=None):
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
        return super().dispatch(request, *args, **kwargs)  

class UserLogoutView(RedirectView):
    template_name = 'auth/auth_login.html'
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('user:auth_login')
    

class AvatarUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = AvatarUpdateForm
    template_name = 'user/update_avatar.html'
    success_url = reverse_lazy('user:user_profile') 
    def get_object(self):
        return self.request.user


    
class PasswordResetView(DjangoPasswordResetView):
    template_name = 'ps_reset/password_reset_form.html'
    email_template_name = 'ps_reset/password_reset_email.html'
    subject_template_name = 'ps_reset/password_reset_subject.txt'
    success_url = reverse_lazy('user:password_reset_done')

    def get_email_context(self):
        context = super().get_email_context()
        context['domain'] = '127.0.0.1:3000'  
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cambiar contraseña'
        return context