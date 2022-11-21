from django import forms
from.models import Post,Category, Comment,Forbidden, Tag
from django.forms.models import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username","email","password1","password2"]
    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','category','tags','picture','content'] #tags #category


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


#======================================================================

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields= ['name']

#======================================================================

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields= ['content']

#======================================================================

class ForbiddenForm(forms.ModelForm):
    class Meta:
        model = Forbidden
        fields= ['word']

#======================================================================

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields= ['name']