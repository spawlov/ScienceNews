from blog.models import Category


def get_categories(request):
    menu_category = Category.objects.all()
    return {"menu_category ": menu_category}
