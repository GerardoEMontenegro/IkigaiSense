from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import re

User = get_user_model()


class AvatarUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar']

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