# Generated by Django 5.1.2 on 2024-10-23 17:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_article_created_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='created_at',
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.CharField(default='General', max_length=100),
        ),
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='articles/'),
        ),
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
