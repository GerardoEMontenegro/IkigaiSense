from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import get_object_or_404, render, redirect
from apps.post.models import Post, PostImage, Comment, Category
from apps.post.forms import PostUpdateForm, PostFilterForm, CommentForm, PostCreateForm
from django.db.models import Count 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  #obliga al usuario a estar logueado para acceder a ciertas vistas
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied 
from django.utils.dateparse import parse_date 

class PostListView(ListView):
    model = Post
    template_name = 'post/post_list.html'
    context_object_name = "posts"

    paginate_by = 5   # Número de posts por página

    def get_queryset(self):
        queryset = Post.objects.all().annotate(comments_count=Count('comments'))   # Anota el número de comentarios por post
        print("GET DATA:", self.request.GET)
        search_query = self.request.GET.get('search_query', '')   # Filtra por título o autor si se proporciona una consulta de búsqueda
        order_by = self.request.GET.get('order_by', '-created_at')   # Ordena por fecha de creación por defecto
        category_id = self.request.GET.get('category', None)   # Filtra por categoría si se proporciona
        comentarios_min = self.request.GET.get('comentarios_min', None)   # Filtra por número mínimo de comentarios si se proporciona
        comentarios_max = self.request.GET.get('comentarios_max', None)   # Filtra por número máximo de comentarios si se proporciona
        fecha_publicacion = self.request.GET.get('fecha_publicacion', None)   # Filtra por fecha de publicación si se proporciona


        if search_query:   # Filtra por título o autor si se proporciona una consulta de búsqueda
            queryset = queryset.filter(title__icontains=search_query) | queryset.filter(
                author__username__icontains=search_query)
            
        if category_id:    # Filtra por categoría si se proporciona
            queryset = queryset.filter(category_id=category_id) # Filtra por categoría si se proporciona

        if fecha_publicacion:  # Filtra por fecha de publicación si se proporciona
            fecha = parse_date(fecha_publicacion)   # Convierte la cadena de fecha en un objeto date
            if fecha:
                queryset = queryset.filter(created_at__date=fecha)

        if comentarios_min:   # Filtra por número mínimo de comentarios si se proporciona
            try:
                min_count = int(comentarios_min)
                queryset = queryset.filter(comments_count__gte=min_count)
            except ValueError:
                pass  # Ignora si no es un número válido

        if comentarios_max:   # Filtra por número máximo de comentarios si se proporciona
            try:
                max_count = int(comentarios_max)
                queryset = queryset.filter(comments_count__lte=max_count)
            except ValueError:
                pass  # Ignora si no es un número válido

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories_with_posts = Category.objects.annotate(post_count=Count('post')).filter(post_count__gt=0)   # Obtiene las categorías que tienen al menos un post

        context['filter_form'] = PostFilterForm(self.request.GET)
        context['categories'] = categories_with_posts

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

class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name = 'post/post_update.html'
    success_url = reverse_lazy('post:post_list')  #herenecia de UpdateView para actualizar un post

    def test_func(self):   #herenecia de UpdateView para actualizar un post
        post = self.get_object()   # Obtiene el post a actualizar
        return post.author == self.request.user   # Verifica si el autor del post es el usuario actual
    
    def form_valid(self, form):
        response = super().form_valid(form)  # Guarda el post (self.object)
        images = self.request.FILES.getlist('images')
        for image in images:
          PostImage.objects.create(post=self.object, image=image)
        return response
    
    def get_context_data(self, **kwargs):   #herenecia de UpdateView para actualizar un post
        context = super().get_context_data(**kwargs)   # Obtiene el contexto de la vista
        context['post'] = self.object   # Añade el post al contexto
        return context   

    
    def get_success_url(self):   #herenecia de UpdateView para actualizar un post
        return reverse_lazy('post:post_list')   #herenecia de UpdateView para actualizar un post

LOGIN_URL = reverse_lazy('user:auth_login')

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post   #herenecia de DeleteView para eliminar un post
    template_name = 'post/post_delete.html'
    success_url = reverse_lazy('post:post_l') # Redirige a la lista de posts después de eliminar

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
