from django.urls import path
from apps.post import views as views

app_name = 'post' 

urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='post_list'),  # Lista de posts
    path('posts/create/', views.PostCreateView.as_view(), name='post_create'),   # Vista para crear un nuevo post
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),    # Detalle de un post específico
    path('posts/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),   # Vista para eliminar un post específico
    path('posts/<slug:slug>/update/', views.PostEditView.as_view(), name='post_update'),   # Vista para actualizar un post específico
    path('post/<slug:slug>/calificar/', views.RatePostView.as_view(), name='post_rating'),
    path('comment/<uuid:pk>/like/', views.CommentLikeToggleView.as_view(), name='comment_like_toggle')


]