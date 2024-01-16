from django.db import models
from django.urls import reverse

from ckeditor.fields import RichTextField


class Category(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="название",
    )
    slug = models.SlugField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        verbose_name="url",
    )

    class Meta:
        verbose_name = "категория(ю)"
        verbose_name_plural = "категории"
        ordering = ("title",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("category", kwargs={"slug": self.slug})


class Tag(models.Model):
    title = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="название",
    )
    slug = models.SlugField(
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        verbose_name="url",
    )

    class Meta:
        verbose_name = "тег(и)"
        verbose_name_plural = "теги"
        ordering = ("title",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("tag", kwargs={"slug": self.slug})


class Post(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="название",
    )
    slug = models.SlugField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        verbose_name="url",
    )
    author = models.CharField(
        max_length=100,
        verbose_name="автор",
    )
    content = RichTextField(
        blank=True,
        null=True,
        verbose_name="контент",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="опубликовано",
    )
    photo = models.ImageField(
        upload_to="photos/%Y/%m/%d",
        blank=True,
        null=True,
        verbose_name="фото",
    )
    views = models.IntegerField(
        default=0,
        verbose_name="количество просмотров",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="categories",
        verbose_name="категория",
    )
    tag = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="tags",
        verbose_name="теги",
    )

    class Meta:
        verbose_name = "статья(ю)"
        verbose_name_plural = "статьи"
        ordering = ("-created_at",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post", kwargs={"slug": self.slug})
