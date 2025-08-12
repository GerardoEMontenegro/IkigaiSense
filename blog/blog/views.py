from django.views.generic import TemplateView
from django.shortcuts import redirect
from apps.post.models import Post
from apps.post.forms import PostForm

class BlogIndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(approved_post=True).order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Asegurate que esté logueado
            post.slug = post.title.replace(" ", "-").lower()
            post.approved_post = True  # Opcional: para desarrollo
            post.save()
            return redirect("home")
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)