from ckeditor_uploader.widgets import CKEditorUploadingWidget

from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from transliterate import slugify

from .models import Category, Post, Tag


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = ("title",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
    )
    fields = ("title",)
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            obj.slug = slugify(form.cleaned_data["title"], language_code="ru")
            obj.save()


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
    )
    fields = ("title",)
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            obj.slug = slugify(form.cleaned_data["title"], language_code="ru")
            obj.save()


class PostAdmin(admin.ModelAdmin):
    save_on_top = True
    form = PostAdminForm
    list_display = (
        "id",
        "title",
        "slug",
        "category",
        "created_at",
        "views",
        "get_list_photo",
        "published",
    )
    list_display_links = (
        "id",
        "title",
    )
    search_fields = ("title",)
    list_filter = ("category",)
    readonly_fields = (
        "views",
        "created_at",
        "get_photo",
    )
    fields = (
        "title",
        "category",
        "tag",
        "content",
        "photo",
        "get_photo",
        "views",
        "created_at",
        "published",
    )
    list_per_page = 10

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(
                f'<img src="{obj.photo.url}" '
                f'style="max-height: '
                f'200px;"><figcaption>{obj.photo_caption}</figcaption>'
            )
        return "-"

    def get_list_photo(self, obj):
        if obj.photo:
            return mark_safe(
                f'<img src="{obj.photo.url}" ' f'style="max-height: 50px;">'
            )
        return "-"

    get_photo.short_description = get_list_photo.short_description = "превью"

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            if not obj.author:
                user = request.user
                obj.author = f"{user.last_name} {user.first_name}".strip()
            obj.slug = slugify(form.cleaned_data["title"], language_code="ru")
            obj.save()


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
