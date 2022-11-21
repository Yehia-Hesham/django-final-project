

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import reverse,get_object_or_404
# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering =('created_at',)

    def __str__(self):
        return f"{self.name}"


    @classmethod
    def get_object(cls, id):
        return get_object_or_404(cls, pk=id)

    @classmethod
    def delete_object(cls, id):
        deleted_object= cls.get_object(id)
        deleted_object.delete()
        return True


    def get_show_url(self):
        return reverse("tag.description",args=[self.id])

    def get_edit_url(self):
        edit_url = reverse("tag.edit",args=[self.id])
        return edit_url

    def get_delete_url(self):
        delete_url = reverse("tag.delete",args=[self.id])
        return delete_url

        
#===================================================================================================

class Category(models.Model):
    name = models.CharField(max_length=100)
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True, related_name='category_sub')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_object(cls, id):
        return get_object_or_404(cls, pk=id)

    @classmethod
    def delete_object(cls, id):
        deleted_object= cls.get_object(id)
        deleted_object.delete()
        return True
        
    def subscribe_button(self,user):
        if user in self.subscribers.all():
            self.subscribers.remove(user)
        else:
            self.subscribers.add(user)

    def get_edit_url(self):
        edit_url = reverse("category.edit",args=[self.id])
        return edit_url

    def get_delete_url(self):
        delete_url = reverse("category.delete",args=[self.id])
        return delete_url

    def get_show_url(self):
        return reverse("category.description",args=[self.id])

    def __str__(self):
        return self.name

#===================================================================================================

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True, blank=True)
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='post/images/',height_field=None, width_field=None,null=True,blank=True)
    content = models.TextField()
    likes = models.ManyToManyField(User,blank=True, related_name='post_like')
    dislikes = models.ManyToManyField(User,blank=True, related_name='post_dislike')
    tags = models.ManyToManyField(Tag,blank=True, related_name='tag_post')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_object(cls, id):
        return get_object_or_404(cls, pk=id)

    @classmethod
    def delete_object(cls, id):
        deleted_object= cls.get_object(id)
        deleted_object.delete()
        return True

    def no_of_likes(self):
        return self.likes.all().count()

    def is_liked(self, user = None):
        if user:
            user_liked = self.likes.filter(user)
        return bool(user_liked)

    def no_of_dislikes(self):
        return self.dislikes.all().count()

    def is_disliked(self, user = None):
        if user:
            user_disliked = self.dislikes.filter(user)
        return bool(user_disliked)

    def like_button(self, user = None):
        user_liked = self.likes.filter(id=user.id) 
        user_disliked = self.dislikes.filter(id=user.id) 
        if user_disliked:
            self.dislikes.remove(user)
        if user_liked:
            self.likes.remove(user)
        else:
            self.likes.add(user)

    def dislike_button(self, user):
        user_liked = self.likes.filter(id=user.id) 
        user_disliked = self.dislikes.filter(id=user.id) 
        if user_liked:
            self.likes.remove(user)
        if user_disliked:
            self.dislikes.remove(user)
        else:
            self.dislikes.add(user)

        if self.no_of_dislikes() >= 10:
            self.delete()
        
    def get_image_url(self):
        return f"/media/{self.picture}"

    def get_edit_url(self):
        edit_url = reverse("post.edit",args=[self.id])
        return edit_url

    def get_delete_url(self):
        delete_url = reverse("post.delete",args=[self.id])
        return delete_url

    def get_show_url(self):
        return reverse("post.description",args=[self.id])

    def __str__(self):
        return self.title

#===================================================================================================

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering =('created_at',)

    def __str__(self):
        return f"{self.author.username}: {self.content}"


    @classmethod
    def get_object(cls, id):
        return get_object_or_404(cls, pk=id)

    @classmethod
    def delete_object(cls, id):
        deleted_object= cls.get_object(id)
        deleted_object.delete()
        return True

    def get_post_url(self):
        return reverse("post.description",args=[self.post.id])

    def get_show_url(self):
        return reverse("comment.description",args=[self.id])

    def get_edit_url(self):
        edit_url = reverse("comment.edit",args=[self.id])
        return edit_url

    def get_delete_url(self):
        delete_url = reverse("comment.delete",args=[self.id])
        return delete_url


    def clean_comment(self):
        forbiddens = Forbidden.objects.all()
        result = self.content
        for forb in forbiddens:
            result = result.replace(forb.word,"*"*len(forb.word))
        return result
    
    def save(self,*args,**kwargs):
        self.content = self.clean_comment()
        super(Comment, self).save(*args, **kwargs)
        

#===================================================================================================

class Forbidden(models.Model):
    word = models.CharField(max_length=100)

    @classmethod
    def get_object(cls, id):
        return get_object_or_404(cls, pk=id)

    @classmethod
    def delete_object(cls, id):
        deleted_object= cls.get_object(id)
        deleted_object.delete()
        return True

    def get_show_url(self):
        return reverse("forbidden.description",args=[self.id])

    def get_edit_url(self):
        edit_url = reverse("forbidden.edit",args=[self.id])
        return edit_url

    def get_delete_url(self):
        delete_url = reverse("forbidden.delete",args=[self.id])
        return delete_url

    def save(self,*args,**kwargs):
        comments = Comment.objects.all()
        for comment in comments:
            comment.save()
        super(Forbidden, self).save(*args, **kwargs)

#===================================================================================================
