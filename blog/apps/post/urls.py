from django.urls import path
from apps.post import views as views

app_name = 'post' # Define el espacio de nombres para las URLs de la aplicación post

urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='post_list'),  # Lista de posts
    path('posts/create/', views.PostCreateView.as_view(), name='post_create'),   # Vista para crear un nuevo post
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),    # Detalle de un post específico
    path('posts/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),   # Vista para eliminar un post específico
    path('posts/<slug:slug>/update/', views.PostUpdateView.as_view(), name='post_update'),   # Vista para actualizar un post específico

    path('posts/<slug:slug>/comments/create/', views.CommentCreateView.as_view(), name='comment_create'),   # Vista para crear un nuevo comentario en un post
    path('comments/<uuid:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),   # Vista para actualizar un comentario específico
    path('comments/<uuid:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),   # Vista para eliminar un comentario específico

]