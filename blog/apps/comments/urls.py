from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('comments/<uuid:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),   
    path('comments/<uuid:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),   

]
