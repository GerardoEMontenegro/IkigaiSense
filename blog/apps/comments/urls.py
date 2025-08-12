# blog/apps/comments/urls.py
from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    # ... otras URLs ...
    path('comment/<uuid:pk>/edit/', views.CommentUpdateView.as_view(), name='comment_edit'),
    path('comment/<uuid:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),

    path('posts/<slug:slug>/comments/create/', views.CommentCreateView.as_view(), name='comment_create'),   # Vista para crear un nuevo comentario en un post
    path('comments/<uuid:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),   # Vista para actualizar un comentario específico
    path('comments/<uuid:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),   # Vista para eliminar un comentario específico

]
