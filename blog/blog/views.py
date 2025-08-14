from django.db.models import Avg, Count
from django.db.models.functions import Coalesce
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.db.models import Q
from apps.post.models import Post
from apps.post.forms import PostFilterForm


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = PostFilterForm(self.request.GET or None)

        posts = Post.objects.annotate(
            average_rating=Coalesce(Avg('ratings__score'), 0.0),
            amount_comments=Count('comments', filter=Q(comments__approved=True))
        ).select_related('author', 'category')

        if form.is_valid():
            search_query = form.cleaned_data.get('search_query')
            category = form.cleaned_data.get('category')
            order_by = form.cleaned_data.get('order_by')

            if search_query:
                posts = posts.filter(
                    Q(title__icontains=search_query) |
                    Q(content__icontains=search_query)
                )

            if category:
                posts = posts.filter(category=category)

            if order_by:
                valid_ordering = ['-created_at', 'created_at', '-amount_comments', '-average_rating']
                if order_by in valid_ordering:
                    posts = posts.order_by(order_by)
                else:
                    posts = posts.order_by('-created_at')
            else:
                posts = posts.order_by('-created_at')
        else:
            posts = posts.order_by('-created_at')

        paginator = Paginator(posts, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['form'] = form
        context['posts'] = page_obj
        context['page_obj'] = page_obj

        return context