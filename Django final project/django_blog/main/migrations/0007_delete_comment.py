# Generated by Django 4.1.3 on 2022-11-15 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_comment_dislikes_comment_likes'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
