# Generated by Django 4.1.3 on 2022-11-18 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_comment_parent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('created_at',)},
        ),
    ]
