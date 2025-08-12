from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings
from django.urls import reverse_lazy
from django.db.models import Avg
from apps.post.forms import PostForm
from apps.post.models import Post, Comment
from apps.comments.forms import CommentForm


class PostListView(ListView):
    model = Post
    template_name = 'post/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.get_object()
        average_rating = post.ratings.aggregate(avg_rating=Avg('score'))['avg_rating']
        context['average_rating'] = average_rating if average_rating else 0
        context['stars'] = range(1, 6)

        context['form'] = CommentForm()
        context['comments'] = Comment.objects.filter(post=post).order_by('-created_at')

        return context



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "El post se creó correctamente.")
        return super().form_valid(form)


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para editar este post.")
        return super().handle_no_permission()

    def form_valid(self, form):
        messages.success(self.request, "El post se actualizó correctamente.")
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para eliminar este post.")
        return super().handle_no_permission()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "El post se eliminó correctamente.")
        return super().delete(request, *args, **kwargs)



