from blog.models import Category, Post


def get_general_context(request):
    menu_category = Category.objects.all()
    popular_posts = Post.objects.all().order_by("-views")[:5]
    return {
        "menu_category": menu_category,
        "five_popular_posts": popular_posts,
    }
