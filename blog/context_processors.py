from .models import Category, Post, Tag


def get_general_context(request):
    menu_category = Category.objects.all()
    return {
        "menu_category": menu_category,
    }
