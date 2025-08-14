from django.contrib import admin
from apps.post.models import Post, Category, Comment, PostImage, Rating


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'author',
        'category',
        'approved_post',
        'created_at',
        'updated_at',
        'allow_comments'
    )
    list_editable = ('approved_post',) 
    search_fields = ('title', 'content', 'author__username')
    list_filter = (
        'approved_post',      
        'category',
        'author',
        'created_at',
        'allow_comments'
    )
    prepopulated_fields = {'slug': ('title',)}  
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Contenido', {
            'fields': ('title', 'slug', 'category', 'author', 'content', 'image')
        }),
        ('Aprobación y comentarios', {
            'fields': ('approved_post', 'allow_comments'),
            'classes': ('collapse',),
            'description': 'Controla la visibilidad del post y si permite comentarios.'
        }),
        ('Fechas (solo lectura)', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    actions = ['approve_posts', 'disapprove_posts']

    @admin.action(description='✅ Aprobar los posts seleccionados')
    def approve_posts(self, request, queryset):
        updated = queryset.update(approved_post=True)
        self.message_user(request, f'{updated} posts han sido aprobados.')

    @admin.action(description='❌ Desaprobar los posts seleccionados')
    def disapprove_posts(self, request, queryset):
        updated = queryset.update(approved_post=False)
        self.message_user(request, f'{updated} posts han sido desaprobados.')



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'created_at', 'approved')
    list_filter = ('approved', 'created_at', 'post', 'author')
    search_fields = ('post__title', 'author__username', 'content')
    list_editable = ('approved',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('post', 'author', 'content')
        }),
        ('Estado', {
            'fields': ('approved',),
        }),
        ('Fechas', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )



@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'image', 'created_at')
    list_filter = ('post', 'created_at')
    search_fields = ('post__title', 'post__id')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)



@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'score', 'created_at')
    list_filter = ('score', 'post', 'user', 'created_at')
    search_fields = ('post__title', 'user__username')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('post', 'user', 'score')
        }),
        ('Fecha', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


admin.site.register(Category, CategoryAdmin)