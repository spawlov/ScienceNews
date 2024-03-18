# Generated by Django 5.0 on 2023-12-21 15:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=255,
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        max_length=255,
                        unique=True,
                        verbose_name="url",
                    ),
                ),
            ],
            options={
                "ordering": ("title",),
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=50,
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        unique=True,
                        verbose_name="url",
                    ),
                ),
            ],
            options={
                "ordering": ("title",),
            },
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=255,
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        max_length=255,
                        unique=True,
                        verbose_name="url",
                    ),
                ),
                (
                    "author",
                    models.CharField(
                        max_length=100,
                    ),
                ),
                (
                    "content",
                    models.TextField(
                        blank=True,
                        null=True,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="опубликовано",
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        upload_to="photos/%Y/%m/%d",
                    ),
                ),
                (
                    "views",
                    models.IntegerField(
                        default=0,
                        verbose_name="количество просмотров",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="posts",
                        to="blog.category",
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        blank=True,
                        related_name="posts",
                        to="blog.tag",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
            },
        ),
    ]
