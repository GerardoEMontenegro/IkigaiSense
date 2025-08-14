from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import os

def get_avatar_filename(instance, filename):
    base_filename , file_extension = os.path.splitext(filename)
    new_filename = f"user_{instance.id}_avatar{file_extension}"
    return os.path.join('user/avastar/', new_filename)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    alias = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to=get_avatar_filename, default='user/default/default-avatar.png')

    def __str__(self):
        return self.username
  
    @property
    def is_registered(self):
        return self.groups.filter(name='Registered').exists()
  
    @property
    def is_collaborator(self):
        return self.groups.filter(name='Collaborator').exists()
  
    @property
    def is_admin(self):
        return self.groups.filter(name='Admin').exists()
    
    def get_avartar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return None

# Create your models here.
