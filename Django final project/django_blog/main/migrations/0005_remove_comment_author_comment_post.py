# Generated by Django 4.1.3 on 2022-11-15 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_category_comment_post_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.post'),
        ),
    ]
