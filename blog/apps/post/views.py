from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import get_object_or_404, render, redirect
from apps.post.models import Post, Comment
from apps.post.forms import ImageFormSet, CommentForm
from apps.post.forms import PostForm, PostFilterForm, CommentForm
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied 

class PostListView(ListView):
    model = Post
    template_name = 'post/post_list.html'
    context_object_name = "posts"

    paginate_by = 5   # Número de posts por página

    def get_queryset(self):
        queryset = Post.objects.all().annotate(comments_count=Count('comments'))
        search_query = self.request.GET.get('search_query', '')
        order_by = self.request.GET.get('order_by', '-created_at')

        if search_query:
            queryset = queryset.filter(title__icontains=search_query) | queryset.filter(
                author__username__icontains=search_query)

        return queryset.order_by(order_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = PostFilterForm(self.request.GET)

        if context.get('is_paginated', False):
            query_params = self.request.GET.copy()
            query_params.pop('page', None)

            pagination = {}
            page_obj = context['page_obj']
            paginator = context['paginator']

            if page_obj.number > 1:
                pagination['first_page'] = f'?{query_params.urlencode()}&page={paginator.page_range[0]}'

            if page_obj.has_previous():
                pagination['previous_page'] = f'?{query_params.urlencode()}&page={page_obj.number - 1}'

            if page_obj.has_next():
                pagination['next_page'] = f'?{query_params.urlencode()}&page={page_obj.number + 1}'

            if page_obj.number < paginator.num_pages:
                pagination['last_page'] = f'?{query_params.urlencode()}&page={paginator.num_pages}'

            context['pagination'] = pagination

        return context

class PostDetailView(DetailView): #herenecia de TemplateView para crear una vista de detalle del post
    model = Post
    template_name = 'post/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_images = self.object.images.filter(active=True)

        context['active_images'] = active_images
        context['add_comment_form'] = CommentForm()

        edit_comment_id = self.request.GET.get('edit_comment')
        if edit_comment_id:
            comment = get_object_or_404(Comment, id=edit_comment_id)

            if comment.author == self.request.user:
                context['editing_comment_id'] = comment.id
                context['edit_comment_form'] = CommentForm(instance=comment)
            else:
                context['editing_comment_id'] = None
                context['edit_comment_form'] = None

        delete_comment_id = self.request.GET.get('delete_comment')
        if delete_comment_id:
            comment = get_object_or_404(Comment, id=delete_comment_id)

            if (comment.author == self.request.user or
                    (comment.post.author == self.request.user and not
                     comment.author.is_admin and not
                     comment.author.is_superuser) or
                    self.request.user.is_superuser or
                    self.request.user.is_staff or
                    self.request.user.is_admin
                ):
                context['deleting_comment_id'] = comment.id
            else:
                context['deleting_comment_id'] = None

        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post/post_create.html'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            if 'images_formset' not in context:
                context['images_formset'] = ImageFormSet(instance=self.object if self.object else Post())
            return context

    def form_valid(self, form):
        user = self.request.user
        titulo = form.cleaned_data['title']
        contenido = form.cleaned_data['content']

        palabras_prohibidas = ['spam', 'prohibido', 'baneo']
        if any(p in titulo.lower() for p in palabras_prohibidas):
            form.add_error('title', 'El título contiene palabras no permitidas.')
            return self.form_invalid(form)

        if len(contenido) < 100:
            form.add_error('content', 'El contenido debe tener al menos 100 caracteres.')
            return self.form_invalid(form)

        hoy = now().date()
        posts_hoy = Post.objects.filter(author=user, created_at__date=hoy).count()
        if posts_hoy >= 3:
            form.add_error(None, "Ya has publicado el máximo de 3 posts hoy.")
            return self.form_invalid(form)

        form.instance.author = user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post:post_detail', kwargs={'slug': self.object.slug})

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post/post_update.html'

    def test_func(self):   #herenecia de UpdateView para actualizar un post
        post = self.get_object()   # Obtiene el post a actualizar
        return post.author == self.request.user   # Verifica si el autor del post es el usuario actual

    def get_success_url(self):   #herenecia de UpdateView para actualizar un post
        return reverse_lazy('post:post_detail', kwargs={'slug': self.object.slug})   #herenecia de UpdateView para actualizar un post

class PostDeleteView(DeleteView):
    model = Post   #herenecia de DeleteView para eliminar un post
    template_name = 'post/post_delete.html'
    success_url = reverse_lazy('post:post_list') # Redirige a la lista de posts después de eliminar

    def get_context_data(self, **kwargs): # Método para obtener el contexto de la vista
        context = super().get_context_data(**kwargs)   #herenecia de DeleteView para eliminar un post
        slug = self.kwargs.get('slug')   # Obtiene el slug del post a eliminar
        post = get_object_or_404(Post, slug=slug, author=self.request.user)  # Obtiene el post a eliminar
        context['post'] = post   # Añade el post al contexto
        return context   

    def post(self, request, *args, **kwargs): # Manejo del formulario de eliminación del post
        slug = self.kwargs.get('slug')
        post = get_object_or_404(Post, slug=slug, author=request.user)   #herenecia de DeleteView para eliminar un post
        post.delete()
        return redirect('post:post_list')  # Redirige a la lista de posts después de eliminar

class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'post/post_detail.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(slug=self.kwargs['slug'])

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post:post_detail', kwargs={'slug': self.object.post.slug})
    
class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'post/post_detail.html'

    def get_object(self, queryset=None):
        comment = super().get_object(queryset)
        if comment.author != self.request.user:
            raise PermissionDenied("No tienes permiso para editar este comentario.")
        return comment

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post:post_detail', kwargs={'slug': self.object.post.slug})

class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'post/post_detail.html'

    def get_object(self, queryset=None):
        comment = super().get_object(queryset)
        if (comment.author != self.request.user and
            comment.post.author != self.request.user and
            not self.request.user.is_superuser and
            not self.request.user.is_staff and
            not self.request.user.is_admin):
            raise PermissionDenied("No tienes permiso para eliminar este comentario.")
        return comment

    def get_success_url(self):
        return reverse_lazy('post:post_detail', kwargs={'slug': self.object.post.slug})
