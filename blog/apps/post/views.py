from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import get_object_or_404, render, redirect
from apps.post.models import Post, PostImage, Comment, Category
from apps.post.forms import PostForm, PostFilterForm, CommentForm, PostCreateForm, CategoryForm
from django.db.models import Count
#from django.contrib.auth.mixins import LoginRequiredMixin  #obliga al usuario a estar logueado para acceder a ciertas vistas
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

class PostCreateView(CreateView):
    model = Post
    form_class = PostCreateForm 
    template_name = 'post/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save()

        images = self.request.FILES.getlist('images')

        if images:
            for image in images:
                PostImage.objects.create(post=post, image=image)
        else:
            PostImage.objects.create(
                post=post, image=settings.DEFAULT_POST_IMAGE)

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

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_create.html'
    success_url = reverse_lazy('category_list')  # Reemplaza con la URL de redirección deseada

class CategoryListView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_list.html'
    success_url = reverse_lazy('category_list')  