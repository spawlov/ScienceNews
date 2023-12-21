from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin

from .models import Category, Tag, Post


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    form = PostAdminForm


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
