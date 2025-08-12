from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import os


def get_avatar_filename(instance, filename):
    # avatar_default.jpg

    base_filename, file_extension = os.path.splitext(filename)
    new_filename = f"user_{instance.id}_avatar{file_extension}" 
    
    return os.path.join('user/avatar/', new_filename)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    alias = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, null=False)
    avatar = models.ImageField(upload_to=get_avatar_filename, default='user/default/default-avatar-2.png') #MODELO CON UNA SOLA IMAGEN)
    
    def __str__(self):
        return self.username

    @property
    def is_registered(self):
        return self.groups.filter(name='registered').exists()   # This method checks if the user is part of the 'registered' group

    @property
    def is_colaborator(self):
        return self.groups.filter(name='Colaborator').exists()
    @property
    def is_admin(self):
        return self.groups.filter(name='Admin').exists()
    
def get_avatar_url(self):
    if self.avatar and hasattr(self.avatar, 'url'):
        return self.avatar.url
    return None