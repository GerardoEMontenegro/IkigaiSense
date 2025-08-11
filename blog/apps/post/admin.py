from django.contrib import admin
from apps.post.models import Post, Comment, PostImage, Category #importando los modelos


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)  # Muestra el campo 'title' en la lista de categorías
    search_fields = ('title',)  # Permite buscar por el campo 'title'

admin.site.register(Category, CategoryAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at', 'approved_post')
    search_fields = ('title', 'content', 'author__username')  # Permite buscar por título, contenido y nombre de usuario del autor
    list_filter = ('created_at', 'updated_at', 'author', 'category',  'approved_post')  # Filtros para la lista de posts
    prepopulated_fields = {'slug': ('title',)}  # Genera automáticamente el slug a partir del título
    ordering = ('-created_at',)  # Ordena los posts por fecha de creación de forma descendente
    actions = ['activate_comments', 'deactivate_comments']  # Acciones personalizadas para activar/desactivar comentarios
    
    def activate_comments(modeladmin, request, queryset): #activo comentarios
        update = queryset.update(allow_comments=True)
        modeladmin.message_user(request, f"{update} los comentarios fueron activados correctamente.")
    
    activate_comments.short_description = "Activar comentarios seleccionados"
    
    def deactivate_comments(modeladmin, request, queryset): #desactivo comentarios
        update = queryset.update(allow_comments=False)
        modeladmin.message_user(request, f"{update} los comentarios fueron desactivados correctamente.")
   
    deactivate_comments.short_description = "Desactivar comentarios seleccionados"

admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'updated_at')
    search_fields = ('content',)
    list_filter = ('created_at', 'updated_at')

    def activate_images(modeladmin, request, queryset):
        update = queryset.update(active=True)
        modeladmin.message_user(request, f"{update} las imagenes fueron activadas correctamente.")
    
    activate_images.short_description = "Activar imagenes seleccionadas"

    def deactivate_images(modeladmin, request, queryset):
        update = queryset.update(active=False)
        modeladmin.message_user(request, f"{update} las imagenes fueron desactivadas correctamente.")

    deactivate_images.short_description = "Desactivar imagenes seleccionadas"

admin.site.register(Comment, CommentAdmin)

class PostImageAdmin(admin.ModelAdmin):
    list_display = ('post', 'image', 'active', 'created_at')  # Muestra los campos 'post', 'image', 'active' y 'created_at'
    search_fields = ('post__title', 'author__username', 'post__title')  # Permite buscar por el título del post asociado
    list_filter = ('post',)   # Filtro para el post asociado
    actions = ['activate_images', 'deactivate_images']  # Acciones personalizadas para activar/desactivar imágenes

admin.site.register(PostImage, PostImageAdmin)   # Registra el modelo PostImage en el admin de Django
