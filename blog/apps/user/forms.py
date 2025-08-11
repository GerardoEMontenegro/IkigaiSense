from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from apps.user.models import User
from django import forms
from django.contrib.auth import get_user_model
import re



User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    alias = forms.CharField(required=False, max_length=30)

    class Meta:
        model = User
        fields = ("username", "alias", "email", "password1", "password2")

    def clean_password1(self):
        password = self.cleaned_data.get("password1")

        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")

        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("La contraseña debe incluir al menos una letra mayúscula.")

        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("La contraseña debe incluir al menos una letra minúscula.")

        if not re.search(r'\d', password):
            raise forms.ValidationError("La contraseña debe incluir al menos un número.")

        return password

class LoginForm(AuthenticationForm): 
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

class AvatarUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar']