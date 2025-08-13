from django.views.generic import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from apps.post.models import Comment
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from apps.comments.forms import CommentForm
from apps.post.models import Post
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin







class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def form_valid(self, form):
        messages.success(self.request, "Comentario actualizado con éxito.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post:post_detail', kwargs={'slug': self.object.post.slug})

    def get(self, request, *args, **kwargs):
        return redirect(self.get_success_url())


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'post/comment_confirm_delete.html'  

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author  # Solo el autor puede eliminar

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Comentario eliminado correctamente.")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
             return reverse_lazy('post:post_detail', kwargs={'slug': self.object.post.slug})