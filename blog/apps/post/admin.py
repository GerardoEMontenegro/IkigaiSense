from django.contrib import admin
from apps.post.models import *




# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'category', 'created_at', 'updated_at', 'allow_comments')
    search_fields = ('title', 'content')
    list_filter = ('category', 'author', 'created_at', 'allow_comments')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'created_at')
    search_fields = ('id', 'author', 'created_at', 'post__title')
    list_filter = ('id', 'author', 'created_at')
    ordering = ('-created_at',)

def active_images():
    pass


class PostImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'image', 'created_at')
    search_fields = ('post__id', 'post__title')
    list_filter = ('post', 'created_at')
    ordering = ('-created_at',)













admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Rating)