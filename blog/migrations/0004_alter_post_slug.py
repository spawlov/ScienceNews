# Generated by Django 5.0 on 2024-01-14 06:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0003_alter_category_options_alter_post_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="slug",
            field=models.SlugField(
                blank=True,
                default="",
                max_length=255,
                null=True,
                unique=True,
                verbose_name="url",
            ),
        ),
    ]
