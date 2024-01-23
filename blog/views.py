from django.core.cache import cache
from django.db.models import F
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView

from .models import Category, Post, Tag


class ContactsView(TemplateView):
    template_name = "blog/contacts.html"


class HomeView(ListView):
    queryset = Post.objects.select_related('category').filter(published=True)
    template_name = "blog/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest"] = self.object_list.order_by("-created_at").first()
        context["latest_list"] = self.object_list.order_by("-created_at")[:10]
        context["most_popular"] = self.object_list.order_by('-views').first()
        context["random_news"] = self.object_list.order_by('?')[:9]
        return context


class PostsListView(ListView):
    queryset = (
        Post.objects.select_related('category')
        .filter(published=True)
        .order_by('-created_at')
    )
    template_name = "blog/posts.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_posts"] = (
            Post.objects
            .select_related('category')
            .prefetch_related('tag')
            .filter(published=True)
            .order_by("-views")[:10]
        )
        tags = []
        for post in context["popular_posts"]:
            for tag in post.tag.all():
                tags.append(tag)
        context["popular_tags"] = set(tags)
        return context


class PostsByCategoryView(ListView):
    template_name = "blog/category.html"
    context_object_name = "categories"
    paginate_by = 10

    def get_queryset(self):
        return get_list_or_404(
            Post,
            category__slug=self.kwargs.get("slug"),
            published=True,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = get_object_or_404(
            Category, slug=self.kwargs.get("slug")
        ).title
        context["popular_posts_by_category"] = (
            Post.objects
            .filter(
                published=True,
                category__slug=self.kwargs.get("slug")
            ).order_by("-views")[:10]
        )
        tags = []
        for post in context["popular_posts_by_category"]:
            for tag in post.tag.all():
                tags.append(tag)
        context["popular_tags"] = set(tags)
        return context


class PostsByTagView(ListView):
    template_name = "blog/tag.html"
    context_object_name = "tags"
    paginate_by = 6

    def get_queryset(self):
        return get_list_or_404(Post, tag__slug=self.kwargs.get("slug"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        context["title"] = get_object_or_404(Tag, slug=slug).title
        context["popular_posts_by_tag"] = (
            Post.objects
            .filter(
                published=True,
                tag__slug=self.kwargs.get("slug")
            ).order_by("-views")[:10]
        )
        tags = []
        for post in context["popular_posts_by_tag"]:
            for tag in post.tag.all():
                tags.append(tag)
        context["popular_tags"] = set(tags)
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/single.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_posts"] = (
            Post.objects
            .select_related('category')
            .prefetch_related('tag')
            .filter(published=True)
            .order_by("-views")[:5]
        )
        tags = []
        for post in context["popular_posts"]:
            for tag in post.tag.all():
                tags.append(tag)
        context["popular_tags"] = set(tags)
        self.object.views = F("views") + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


class SearchView(ListView):
    template_name = "blog/search_results.html"
    context_object_name = "search_results"
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(
            content__icontains=self.request.GET.get("keyword"),
            published=True
        ).order_by("-created_at")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_posts"] = (
            Post.objects
            .select_related('category')
            .prefetch_related('tag')
            .filter(
                content__icontains=self.request.GET.get("keyword"),
                published=True
            )
            .order_by("-views")[:10]
        )
        tags = []
        for post in context["popular_posts"]:
            for tag in post.tag.all():
                tags.append(tag)
        context["popular_tags"] = set(tags)
        return context
