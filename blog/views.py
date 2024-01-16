from django.db.models import F
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.generic import ListView, DetailView

from .models import Post, Category, Tag


class Home(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Classic Blog Design"
        return context


class PostByCategory(ListView):
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        return get_list_or_404(Post, category__slug=self.kwargs.get("slug"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = get_object_or_404(
            Category, slug=self.kwargs.get("slug")
        ).title
        return context


class PostByTag(ListView):
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        return get_list_or_404(Post, tag__slug=self.kwargs.get("slug"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        context["title"] = get_object_or_404(Tag, slug=slug).title
        return context


class PostDetail(DetailView):
    model = Post
    template_name = "blog/post.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F("views") + 1
        self.object.save()
        self.object.refresh_from_db()
        return context
