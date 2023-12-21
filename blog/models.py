from ckeditor.fields import RichTextField
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, verbose_name="url")

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, verbose_name="url")

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, verbose_name="url")
    author = models.CharField(max_length=100)
    content = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="опубликовано")
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    views = models.IntegerField(default=0, verbose_name="количество просмотров")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="posts")
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title
