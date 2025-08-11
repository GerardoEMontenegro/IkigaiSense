# blog/apps/comments/urls.py
from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    # ... otras URLs ...
    path('comment/<uuid:pk>/edit/', views.CommentEditView.as_view(), name='comment_edit'),
    path('comment/<uuid:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
]
