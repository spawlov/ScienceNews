from .models import Category, Post, Tag


def get_general_context(request):
    menu_category = Category.objects.all()
    posts = Post.objects.all()
    tags = Tag.objects.all().order_by("?")[:50]
    popular_posts = posts.order_by("-views")[:5]
    random_post = posts.order_by("?").first()
    return {
        "menu_category": menu_category,
        "five_popular_posts": popular_posts,
        "random_post": random_post,
        "tags_cloud": tags,
    }
