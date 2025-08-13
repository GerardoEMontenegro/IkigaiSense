from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings
from django.urls import reverse_lazy
from django.db.models import Avg, Count
from apps.post.forms import PostForm, PostFilterForm
from apps.post.models import Post, Comment, Rating
from apps.comments.forms import CommentForm
from django.views import View
from django.http import JsonResponse


class PostListView(ListView):
    model = Post
    template_name = 'post/post_list.html'
    context_object_name = "posts"

    paginate_by = 6   # Número de posts por página

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


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'post'

    def get_queryset(self):
      
        return Post.objects.select_related('author', 'category').prefetch_related(
            'comments__author',
            'ratings'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        # Comentarios
        context['comments'] = post.comments.order_by('-created_at')
        context['comment_form'] = CommentForm() if post.allow_comments else None

        # Rating del usuario actual
        user = self.request.user
        user_rating = None
        if user.is_authenticated:
            user_rating = post.ratings.filter(user=user).values_list('score', flat=True).first()
        context['user_rating'] = user_rating or 0  # Asegura que no sea None

        # Estadísticas de rating

        ratings_stats = post.ratings.aggregate(avg=Avg('score'), count=Count('id'))
        avg = ratings_stats['avg'] or 0
        count = ratings_stats['count'] or 0
        context['average_rating'] = round(avg, 1)
        context['ratings_count'] = count

        full_stars = int(avg)
        has_half = (avg - full_stars) >= 0.25 and (avg - full_stars) < 0.75
        empty_stars = 5 - full_stars - (1 if has_half else 0)

        context['full_stars'] = range(full_stars)
        context['half_star'] = has_half
        context['empty_stars'] = range(empty_stars)
        context['stars'] = range(1, 6)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Carga el post

        post = self.object

        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para interactuar.")
            return self.get(request, *args, **kwargs)


        if 'content' in request.POST:
            return self.handle_comment_create(request, post)

        elif 'score' in request.POST:
            return self.handle_rating(request, post)

        elif 'edit_content' in request.POST:
            return self.handle_comment_update(request, post)




        return self.get(request, *args, **kwargs)

    def handle_comment_create(self, request, post):
        if not post.allow_comments:
            messages.error(request, "Los comentarios están desactivados para este post.")
            return self.get(request)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, "✅ ¡Gracias por tu comentario!")
        else:
            messages.error(request, "❌ Hubo un error en tu comentario.")
        return self.get(request)

    def handle_rating(self, request, post):
        score = request.POST.get('score')
        try:
            score = int(score)
            if 1 <= score <= 5:
                rating, created = Rating.objects.update_or_create(
                    user=request.user,
                    post=post,
                    defaults={'score': score}
                )
                action = "actualizada" if not created else "agregada"
                messages.success(request, f"⭐ ¡Tu calificación de {score} estrellas ha sido {action}!")
            else:
                messages.error(request, "La calificación debe ser entre 1 y 5.")
        except (ValueError, TypeError):
            messages.error(request, "Calificación inválida.")
        return self.get(request)

    def handle_comment_update(self, request, post):
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id, author=request.user)
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "✏️ Comentario actualizado.")
        else:
            messages.error(request, "❌ Error al actualizar el comentario.")
        return self.get(request)

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
    template_name = 'post/post_update.html'

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


class RatePostView(LoginRequiredMixin, View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        try:
            score = int(request.POST.get('score'))
            if score < 1 or score > 5:
                raise ValueError
        except (ValueError, TypeError):
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'message': 'Puntuación inválida. Debe ser entre 1 y 5.'
                }, status=400)
            messages.error(request, "Puntuación inválida.")
            return redirect(post.get_absolute_url())

        rating, created = Rating.objects.update_or_create(
            post=post,
            user=request.user,
            defaults={'score': score}
        )

        avg_rating = Rating.objects.filter(post=post).aggregate(
            avg=Avg('score'),
            count=Count('id')
        )
        average = avg_rating['avg'] or 0
        count = avg_rating['count']

        if is_ajax:
            return JsonResponse({
                'success': True,
                'message': 'Tu valoración fue enviada correctamente.',
                'average_rating': round(average, 1),
                'ratings_count': count
            })

        if created:
            messages.success(request, "Gracias por valorar este post.")
        else:
            messages.success(request, "Tu valoración fue actualizada.")
        return redirect(post.get_absolute_url())


class CommentLikeToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        user = request.user

        if user in comment.likes.all():
            comment.likes.remove(user)
            liked = False
        else:
            comment.likes.add(user)
            liked = True

        return JsonResponse({
            'liked': liked,
            'likes_count': comment.likes.count(),
        })