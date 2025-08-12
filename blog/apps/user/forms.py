from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from apps.user.models import User
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(UserCreationForm):   # Formulario para el registro de usuarios
    class Meta: # Meta clase para definir el modelo y los campos del formulario
        model = User # Modelo de usuario
        fields = ('username', 'email', 'alias', 'avatar', 'password1', 'password2') # Campos del formulario: nombre de usuario, email, alias, avatar, contraseña1 y contraseña2
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
        }

class LoginForm(AuthenticationForm): # Formulario para el inicio de sesión
    username = forms.CharField(label='Username or Email', max_length=150, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}))
    password = forms.CharField(label='Password', 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))

class PerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full border rounded p-2'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full border rounded p-2'}),
            'email': forms.EmailInput(attrs={'class': 'w-full border rounded p-2'}),
            'avatar': forms.FileInput(attrs={'class': 'w-full text-sm text-gray-600 '
            'file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-1 file:text-sm '
            'file:font-semibold file:bg-yellow-800 file:text-white hover:file:bg-orange-300'}),
        }