from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from transliterate import slugify

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Category, Tag, Post


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    fields = ('title',)

    def save_model(self, request, obj, form, change):
        obj.slug = slugify(form.cleaned_data['title'], language_code='ru')
        obj.save()


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    fields = ('title',)

    def save_model(self, request, obj, form, change):
        obj.slug = slugify(form.cleaned_data['title'], language_code='ru')
        obj.save()


class PostAdmin(admin.ModelAdmin):
    save_on_top = True
    form = PostAdminForm
    list_display = ('id', 'title', 'slug', 'category', 'created_at', 'views', 'get_list_photo',)
    list_display_links = ('id', 'title',)
    search_fields = ('title',)
    list_filter = ('category',)
    readonly_fields = ('views', 'created_at', 'get_photo',)
    fields = ('title', 'category', 'tags', 'content', 'photo', 'get_photo', 'views', 'created_at',)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" style="max-height: 200px;">')
        return '-'

    def get_list_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" style="max-height: 50px;">')
        return '-'

    get_photo.short_description = get_list_photo.short_description = 'превью'

    def save_model(self, request, obj, form, change):
        obj.slug = slugify(form.cleaned_data['title'], language_code='ru')
        obj.save()


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
