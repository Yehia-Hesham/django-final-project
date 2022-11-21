from django.contrib import admin
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from main.models import Post,Comment,Forbidden
# Register your models here.

# class TheModelAdmin(admin.ModelAdmin):
#     # filter_horizontal = ['likes']

admin.site.register(Comment)
admin.site.register((Post,Forbidden))

mod, created= Group.objects.get_or_create(name='mod')
ct = ContentType.objects.get_for_model(model=Post)
perms = Permission.objects.filter(content_type=ct)
mod.permissions.add(*perms)

ct = ContentType.objects.get_for_model(model=User)
perms = Permission.objects.filter(content_type=ct)
mod.permissions.add(*perms)



default, created= Group.objects.get_or_create(name='default')
ct = ContentType.objects.get_for_model(model=Post)
perms = Permission.objects.filter(content_type=ct)
default.permissions.add(*perms)

banned, created= Group.objects.get_or_create(name='banned')


moderatorone = User.objects.filter(username='moderatorone')
mod.user_set.add(moderatorone.first())



