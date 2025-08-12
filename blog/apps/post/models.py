from django.db import models      # Importando los modelos de Django
from django.conf import settings    # Importando settings para el modelo de usuario
from django.utils import timezone   # Importando timezone para la fecha y hora
from django.utils.text import slugify    # Importando slugify para crear slugs
import uuid    # Importando uuid para generar identificadores unicos
import os    # Importando os para manejar rutas de archivos



class Category(models.Model):      #modelo para categoria de post
    title = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return self.title


class Post(models.Model):     # modelo para los posts
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # Identificador unico para el post
    title = models.CharField(max_length=200) # Titulo del post
    slug = models.SlugField(unique=True, max_length=200, blank=True) # Slug unico para el post
    content = models.TextField(max_length=10000) # Contenido del post
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='posts', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now) # Fecha de creacion
    updated_at = models.DateTimeField(auto_now=True) # Fecha de actualizacion
    allow_comments = models.BooleanField(default=True)
    approved_post = models.BooleanField(default=False) # Aprobacion del post
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)

    def __str__(self):    # metodo para mostrar el titulo del post
        return self.title
    
    @property   
    def amount_comments(self):           #cantidad de comentarios
        return self.comments.count()
    
    @property
    def amount_images(self):             #cantidad de imagenes
        return self.images.count()  #cantidad de imagenes que se muestran en el post

    def generate_unique_slug(self):   # metodo para generar un slug unico
        slug = slugify(self.title)   # Genera un slug a partir del titulo
        unique_slug = slug
        num = 1

        while Post.objects.filter(slug=unique_slug).exists():   # Verifica si el slug ya existe
            unique_slug = f'{slug}-{num}'   # Si existe, agrega un numero al final
            num += 1

        return unique_slug 
    
    
    def save(self, *args, **kwargs):   # metodo para guardar el post
        if not self.slug:   # Si no hay slug, genera uno unico
            self.slug = self.generate_unique_slug()   # Genera un slug unico

        super().save(*args, **kwargs)  # Llama al metodo save de la clase padre

        if not self.images.exists():  # Si no hay imagenes, crea una imagen por defecto
            PostImage.objects.create(post=self, image='post/default/post_default.png')   # Imagen por defecto

class Comment(models.Model):   # modelo para los comentarios de los posts
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:20]  # Muestra los primeros 20 caracteres del contenido del comentario

def get_image_path(instance, filename):   # funcion para obtener la ruta de la imagen
        post_id = instance.post.id
        images_count = instance.post.images.count()
        #miimagen.png
        #miimagen      .png
        __, file_extension = os.path.splitext(filename)  # Obtiene la extension del archivo
        # post_c40380a5-6814-4baa-9f20-4fda0e7b7306_image_1.png
        # post_cda0531d-c803-4d1a-ab85-3203b63dbc01_image_2.png

        # post_35da329c-3284-4076-9b0f-9470d2a5418b_image_1.png
        # post_35da329c-3284-4076-9b0f-9470d2a5418b_image_2.png
        # post_35da329c-3284-4076-9b0f-9470d2a5418b_image_3.png
        new_filename = f"post_{post_id}_image_{images_count + 1}{file_extension}"  # Crea un nuevo nombre de archivo unico
        return os.path.join('post/cover/', new_filename)    

    
class PostImage(models.Model):   # modelo para las imagenes de los posts
    post = models.ForeignKey(    # relacion con el modelo
        Post, on_delete=models.CASCADE, related_name='images')   # relacion con el post que permite acceder a las imagenes del post
    image = models.ImageField(upload_to=get_image_path)   # ruta de la imagen
    active = models.BooleanField(default=True)    # estado de la imagen
    created_at = models.DateTimeField(auto_now_add=True)  # fecha de creacion

    def __str__(self):
        return f"PostImage {self.id}"   