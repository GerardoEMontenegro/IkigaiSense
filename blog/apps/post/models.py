# models.py
from django.db import models
from django.db.models import Avg
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from uuid import uuid4
import os
import uuid

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['title']


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts'
    )
    content = models.TextField(max_length=10000)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    allow_comments = models.BooleanField(default=True)
    approved_post = models.BooleanField(default=False)  # Aprobación del post
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('post:post_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    @property
    def amount_comments(self):
        return self.comments.filter(approved=True).count()  # Si tienes moderación

    @property
    def average_rating(self):
        result = self.ratings.aggregate(avg=Avg('score'))['avg']
        return round(result, 1) if result else 0

    @property
    def ratings_count(self):
        return self.ratings.count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        counter = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{counter}"
            counter += 1
        return unique_slug

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['author']),
            models.Index(fields=['category']),
            models.Index(fields=['created_at']),
            models.Index(fields=['approved_post']),
        ]


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(max_length=500)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    approved = models.BooleanField(default=False)  # Opcional: moderación

    def clean(self):
        if not self.content or not self.content.strip():
            raise ValidationError("El comentario no puede estar vacío.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        short_content = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"{short_content} — {self.author}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        indexes = [
            models.Index(fields=['post']),
            models.Index(fields=['author']),
            models.Index(fields=['created_at']),
            models.Index(fields=['approved']),
        ]


def get_image_path(instance, filename):
    """
    Genera un nombre único para la imagen usando UUID.
    Funciona en creación y edición.
    """
    _, file_extension = os.path.splitext(filename)
    post_id = instance.post.id if instance.post and instance.post.id else "temp"
    unique_id = uuid4().hex[:8]
    new_filename = f"post_{post_id}_img_{unique_id}{file_extension}"
    return os.path.join('post/cover', new_filename)


class PostImage(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to=get_image_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Imagen {self.id} del post '{self.post.title}'"

    class Meta:
        ordering = ['created_at']
        verbose_name = "Imagen del post"
        verbose_name_plural = "Imágenes del post"


class Rating(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        unique_together = ('post', 'user')
        verbose_name = "Puntuación"
        verbose_name_plural = "Puntuaciones"

    def __str__(self):
        return f'{self.user.username} - {self.post.title} - {self.score}'