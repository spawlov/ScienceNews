from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Count, F, Max, Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView

from .models import Category, Post, Subscriber, Tag


class ContactsView(TemplateView):
    template_name = "blog/contacts.html"


class HomeView(ListView):
    queryset = Post.objects.select_related("category").filter(published=True)
    template_name = "blog/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest"] = self.object_list.order_by("-created_at")
        context["popular"] = self.object_list.order_by("-views")
        context["random_news"] = self.object_list.order_by("?")[:6]
        context["popular_categories"] = (
            Category.objects.prefetch_related("categories")
            .annotate(
                new_posts_count=Count(
                    "categories",
                    filter=Q(categories__published=True),
                ),
                latest_post_date=Max(
                    "categories__created_at",
                    filter=Q(categories__published=True),
                ),
            )
            .filter(categories__published=True)
            .order_by("-new_posts_count", "title", "-latest_post_date")[:6]
        )
        return context


class PostsListView(ListView):
    queryset = (
        Post.objects.select_related("category")
        .filter(published=True)
        .order_by("-created_at")
    )
    template_name = "blog/posts.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_posts"] = (
            Post.objects.select_related("category")
            .prefetch_related("tag")
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
        return Post.objects.select_related("category").filter(
            category__slug=self.kwargs.get("slug"),
            published=True,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = get_object_or_404(
            Category, slug=self.kwargs.get("slug")
        ).title
        context["popular_posts_by_category"] = (
            Post.objects.select_related("category")
            .prefetch_related("tag")
            .filter(published=True, category__slug=self.kwargs.get("slug"))
            .order_by("-views")[:10]
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
        return Post.objects.select_related("category").filter(
            tag__slug=self.kwargs.get("slug"),
            published=True,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        context["title"] = get_object_or_404(Tag, slug=slug).title
        context["popular_posts_by_tag"] = (
            Post.objects.select_related("category")
            .prefetch_related("tag")
            .filter(
                published=True,
                tag__slug=self.kwargs.get("slug"),
            )
            .order_by("-views")[:10]
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
            Post.objects.select_related("category")
            .prefetch_related("tag")
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
        queryset = (
            Post.objects.prefetch_related("category")
            .filter(
                content__icontains=self.request.GET.get("keyword"),
                published=True,
            )
            .order_by("-created_at")
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_posts"] = (
            Post.objects.select_related("category")
            .prefetch_related("tag")
            .filter(
                content__icontains=self.request.GET.get("keyword"),
                published=True,
            )
            .order_by("-views")[:10]
        )
        tags = []
        for post in context["popular_posts"]:
            for tag in post.tag.all():
                tags.append(tag)
        context["popular_tags"] = set(tags)
        return context


def add_subscriber(request):
    if request.method == "POST":
        email = request.POST.get("email", "")
        try:
            validate_email(email)
            subscriber, created = Subscriber.objects.get_or_create(email=email)
            if not created:
                request.session["email"] = subscriber.email
            request.session["email"] = email
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        except ValidationError:
            return
