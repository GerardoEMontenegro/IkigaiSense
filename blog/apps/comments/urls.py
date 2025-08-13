from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('comments/edit/<uuid:pk>/', views.CommentUpdateView.as_view(), name='comment_edit'),
    path('comments/<uuid:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),   

]
