<<<<<<< HEAD
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import get_object_or_404, redirect
from apps.post.models import Post, Comment
from apps.post.forms import ImageFormSet, CommentForm
from apps.post.forms import PostForm, PostFilterForm, CommentForm
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
=======
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Avg, Count
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings
>>>>>>> b06bd418632ee89d416d7ea103a626171ba7755a
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied 
from django.utils.timezone import now

from apps.post.models import Post, PostImage, Comment
from apps.post.forms import PostForm, PostFilterForm, ImageFormSet
from apps.comments.forms import CommentForm


class PostListView(ListView):
    model = Post
    template_name = 'post/post_list.html'
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        queryset = Post.objects.all().annotate(comments_count=Count('comments'))
        search_query = self.request.GET.get('search_query', '')
        order_by = self.request.GET.get('order_by', '-created_at')

        if search_query:
            queryset = queryset.filter(title__icontains=search_query) | queryset.filter(
                author__username__icontains=search_query
            )

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


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('comments', 'ratings')

    def get_rating_stats(self, post):
        stats = post.ratings.aggregate(avg=Avg('score'), count=Count('id'))
        return stats['avg'] or 0, stats['count'] or 0

    def get_star_display(self, avg):
        full = int(avg)
        half = 0.25 <= (avg - full) < 0.75
        empty = 5 - full - (1 if half else 0)
        return range(full), half, range(empty)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        user = self.request.user

        # Imágenes activas
        context['active_images'] = post.images.filter(active=True)

        # Comentarios
        context['comments'] = post.comments.order_by('-created_at')
        context['add_comment_form'] = CommentForm() if post.allow_comments else None

        # Editar comentario
        edit_comment_id = self.request.GET.get('edit_comment')
        if edit_comment_id:
            comment = get_object_or_404(Comment, id=edit_comment_id)
            if comment.author == user:
                context['editing_comment_id'] = comment.id
                context['edit_comment_form'] = CommentForm(instance=comment)

        # Eliminar comentario
        delete_comment_id = self.request.GET.get('delete_comment')
        if delete_comment_id:
            comment = get_object_or_404(Comment, id=delete_comment_id)
            if (
                comment.author == user
                or (comment.post.author == user and not comment.author.is_admin and not comment.author.is_superuser)
                or user.is_superuser
                or user.is_staff
                or getattr(user, 'is_admin', False)
            ):
                context['deleting_comment_id'] = comment.id

        # Rating
        context['user_rating'] = None
        if user.is_authenticated:
            rating = post.ratings.filter(user=user).first()
            if rating:
                context['user_rating'] = rating.score

        avg, count = self.get_rating_stats(post)
        full_stars, half_star, empty_stars = self.get_star_display(avg)
        context.update({
            'average_rating': avg,
            'ratings_count': count,
            'full_stars': full_stars,
            'half_star': half_star,
            'empty_stars': empty_stars,
            'stars': [1, 2, 3, 4, 5],
        })

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
        if Post.objects.filter(author=user, created_at__date=hoy).count() >= 3:
            form.add_error(None, "Ya has publicado el máximo de 3 posts hoy.")
            return self.form_invalid(form)

        form.instance.author = user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post:post_detail', kwargs={'slug': self.object.slug})


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post/post_update.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['images_formset'] = ImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['images_formset'] = ImageFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        images_formset = context['images_formset']

        if form.is_valid() and images_formset.is_valid():
            self.object = form.save()
            images_formset.instance = self.object
            images_formset.save()
            messages.success(self.request, "El post y sus imágenes se actualizaron correctamente.")
            return redirect(self.get_success_url())
        else:
            messages.error(self.request, "Hubo errores al actualizar el post. Por favor verifica los formularios.")
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('post:post_detail', kwargs={'slug': self.object.slug})

    def test_func(self):
        user = self.request.user
        post = self.get_object()
        return post.author == user or user.is_superuser or user.is_staff


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post/post_delete.html'
    success_url = reverse_lazy('post:post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        post = get_object_or_404(Post, slug=slug, author=self.request.user)
        context['post'] = post
        return context

    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        post = get_object_or_404(Post, slug=slug, author=request.user)
        post.delete()
<<<<<<< HEAD
        return redirect('post:post_list')  # Redirige a la lista de posts después de eliminar

class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'post/post_detail.html'  # vas a reutilizar la plantilla de detalle

    def dispatch(self, request, *args, **kwargs):
        # Asegurarte de que el post existe, y tenerlo disponible
        self.post = get_object_or_404(Post, slug=kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post
        return super().form_valid(form)

    def get_success_url(self):
        # Redirige otra vez al detalle del post
        return reverse('post:post_detail', kwargs={'slug': self.post.slug})

    def get_context_data(self, **kwargs):
        # Inyecta en el contexto lo mismo que harías en tu DetailView
        context = super().get_context_data(**kwargs)
        context['post'] = self.post
        context['comments'] = self.post.comments.all()
        # el CreateView inyecta por defecto 'form', nosotros lo renombramos
        context['comment_form'] = context['form']
        return context
    
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
=======
        return redirect('post:post_list')
>>>>>>> b06bd418632ee89d416d7ea103a626171ba7755a
