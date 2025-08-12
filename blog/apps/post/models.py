from django.db import models   
from django.db.models import Avg
from django.urls import reverse
from django.conf import settings    
from django.utils import timezone   
from django.utils.text import slugify 
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid    
import os    



class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title
    

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null = True, related_name='posts')
    content = models.TextField(max_length=10000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    allow_comments = models.BooleanField(default=True)
    approved_post = models.BooleanField(default=False) # Aprobacion del post
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('post:post_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
    @property
    def amount_comments(self):
        return self.comments.count()
    
    @property
    def average_rating(self):
        return self.ratings.aggregate(avg=Avg('score'))['avg'] or 0

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

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(max_length=500)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.content
    
def get_image_path(instance, filename):
    post_id = instance.post.id
    images_count = instance.post.images.count()
    _, file_extension = os.path.splitext(filename)
    new_filename = f"post_{post_id}_image_{images_count + 1}{file_extension}"

    return os.path.join('post/cover', new_filename)

    
class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PostImage {self.id}"


class Rating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f'{self.user} - {self.post} - {self.score}'