from blog.models import Category, Post


def get_categories_for_navigate(request):
    menu_category = Category.objects.all()
    return {"menu_category": menu_category}


def get_five_popular_posts(request):
    popular_posts = Post.objects.all().order_by("-views")[:5]
    return {"five_popular_posts": popular_posts}
