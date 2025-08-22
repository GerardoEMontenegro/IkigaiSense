from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.views import View
from django.db import transaction
from apps.post.forms import PostForm, PostFilterForm, CategoryForm
from apps.post.models import Post, Comment, Rating, Category, PostImage
from apps.comments.forms import CommentForm
from .forms import ImageFormSet

class PostListView(ListView):
    model = Post
    template_name = 'post/post_list.html'
    context_object_name = 'posts'  

    def get_queryset(self):
        queryset = Post.objects.filter(approved_post=True).select_related('author', 'category').annotate(
        comments_count=Count('comments'),
        avg_rating=Avg('ratings__score')  
    )
        form = PostFilterForm(self.request.GET)
        if form.is_valid():
            search_query = form.cleaned_data.get('search_query')
            order_by = form.cleaned_data.get('order_by')

            if search_query:
                queryset = queryset.filter(
                    Q(title__icontains=search_query) |
                    Q(content__icontains=search_query) |
                    Q(author__username__icontains=search_query)
                )

            if order_by:
                queryset = queryset.order_by(order_by)
            else:
                queryset = queryset.order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = PostFilterForm(self.request.GET)

        if context.get('is_paginated'):
            query_params = self.request.GET.copy()
            query_params.pop('page', None)
            page_obj = context['page_obj']
            paginator = context['paginator']

            pagination = {}
            if page_obj.number > 1:
                pagination['first_page'] = f'?{query_params.urlencode()}&page=1'
            if page_obj.has_previous():
                pagination['previous_page'] = f'?{query_params.urlencode()}&page={page_obj.previous_page_number()}'
            if page_obj.has_next():
                pagination['next_page'] = f'?{query_params.urlencode()}&page={page_obj.next_page_number()}'
            if page_obj.number < paginator.num_pages:
                pagination['last_page'] = f'?{query_params.urlencode()}&page={paginator.num_pages}'

            context['pagination'] = pagination

        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'object'

    def get_queryset(self):
        return Post.objects.select_related('author', 'category').prefetch_related(
            'comments__author',
            'comments__likes',
            'ratings',
            'images'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        user = self.request.user

        print(f"Usuario: {user}")
        print("Permisos:", user.get_all_permissions())

        comments = post.comments.order_by('-created_at')

        for comment in comments:
            comment.can_edit = comment.author == self.request.user or self.request.user.is_staff

        context['comments'] = comments
        context['comment_form'] = CommentForm() if post.allow_comments else None

        user_rating = None
        if user.is_authenticated:
            user_rating = post.ratings.filter(user=user).first()
        context['user_rating'] = user_rating.score if user_rating else 0

        ratings_stats = post.ratings.aggregate(avg=Avg('score'), count=Count('id'))
        avg = ratings_stats['avg'] or 0
        count = ratings_stats['count']

        context['average_rating'] = round(avg, 1)
        context['ratings_count'] = count

        full_stars = int(avg)
        has_half = 0.25 <= (avg - full_stars) < 0.75
        empty_stars = 5 - full_stars - (1 if has_half else 0)

        context['full_stars'] = range(full_stars)
        context['half_star'] = has_half
        context['empty_stars'] = range(empty_stars)
        context['stars'] = range(1, 6)

        return context
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        post = self.object

        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para interactuar.")
            return self.get(request)

        if 'content' in request.POST:
            return self.handle_comment_create(request, post)

        elif 'score' in request.POST:
            return self.handle_rating(request, post)

        elif 'edit_content' in request.POST:
            return self.handle_comment_update(request, post)

        return self.get(request, *args, **kwargs)

    def handle_comment_create(self, request, post):
        if not post.allow_comments:
            messages.error(request, "Los comentarios están desactivados.")
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
                Rating.objects.update_or_create(
                    user=request.user,
                    post=post,
                    defaults={'score': score}
                )
                messages.success(request, "⭐ Calificación guardada.")
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['images_formset'] = ImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['images_formset'] = ImageFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        images_formset = context['images_formset']
        form.instance.author = self.request.user

        if images_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                images_formset.instance = self.object
                images_formset.save()
            messages.success(self.request, "El post se creó correctamente.")
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post/post_update.html'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'

    def test_func(self):
        post = self.get_object()
        return (
            self.request.user.is_superuser or
            self.request.user.is_admin or
            self.request.user.is_collaborator or
            self.get_object().author == self.request.user
        )

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

        delete_images_ids = self.request.POST.getlist('delete_images')

        if images_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()

                images_formset.instance = self.object
                images_formset.save()

                if delete_images_ids:
                    PostImage.objects.filter(id__in=delete_images_ids, post=self.object).delete()

            messages.success(self.request, "El post se actualizó correctamente.")
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('post:post_detail', kwargs={'slug': self.object.slug})



class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'post/post_confirm_delete.html' 
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para eliminar este post.")
        return super().handle_no_permission()

    def delete(self, request, *args, **kwargs):
        messages.success(request, "El post se eliminó correctamente.")
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

        Rating.objects.update_or_create(
            post=post,
            user=request.user,
            defaults={'score': score}
        )

        avg_rating = Rating.objects.filter(post=post).aggregate(avg=Avg('score'), count=Count('id'))
        average = avg_rating['avg'] or 0
        count = avg_rating['count']

        if is_ajax:
            return JsonResponse({
                'success': True,
                'message': 'Tu valoración fue enviada correctamente.',
                'average_rating': round(average, 1),
                'ratings_count': count
            })

        messages.success(request, "Gracias por tu valoración.")
        return redirect(post.get_absolute_url())


class CommentLikeToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        user = request.user
        liked = user in comment.likes.all()

        if liked:
            comment.likes.remove(user)
        else:
            comment.likes.add(user)

        return JsonResponse({
            'liked': not liked,
            'likes_count': comment.likes.count(),
        })


class CategoryCreateView(View):
    template_name = 'category/category_create.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('title')  
        if name:
          
            Category.objects.create(title=name)
            messages.success(request, "Categoría creada correctamente.")
            return redirect('post:category_create')
        else:
            messages.error(request, "El nombre de la categoría no puede estar vacío.")
            return render(request, self.template_name)


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'post/category_list.html'
    context_object_name = 'categories'

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'post/category_delete.html'
    success_url = reverse_lazy('category_list.html')