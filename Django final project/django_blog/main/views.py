from time import time

from .forms import RegisterationForm, PostForm, CommentForm,\
                   UpdateUserForm, CategoryForm, ForbiddenForm, TagForm
from .models import Post, Category, Comment,Forbidden,Tag
from .admin import mod, default
from.templatetags.has_group import has_group

from django.http import HttpResponse
from django import template
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout, authenticate

# Create your views here.


#====================================================================== HOME
# @login_required(login_url='/login')
def home(request):
    if len(request.user.groups.filter(name='banned')):
        return HttpResponse(f"<h1>Your account ({request.user.username}) is Banned, please contact admin </h1>")
    if request.user.is_authenticated:
        subbed_cats = Category.objects.filter(subscribers__in=[request.user])
        print("new render: =======\n","current subbed cats:")
        for cat in subbed_cats:
            print(f"-- {cat.name}")
    else:
        subbed_cats = None
    
    if subbed_cats:
        posts = []
        for cat in subbed_cats:
            cat_posts = Post.objects.filter(category=cat).order_by('created_at')
            for post in cat_posts:
                posts.append(post)
    else:
        posts = Post.objects.all().order_by('created_at')
    limit = 5
    end = len(posts) if len(posts) <= limit else limit
    posts = posts[:end]
    categories = Category.objects.all()

    if request.POST:
        if request.user.is_authenticated and "subscribe-cat-id" in request.POST:
            cat_id = request.POST.get("subscribe-cat-id")
            cat = Category.get_object(id=cat_id)
            if request.user in cat.subscribers.all():
                cat.subscribers.remove(request.user)
            else:
                cat.subscribers.add(request.user)
        if request.user.is_authenticated and "post-id" in request.POST:
            post_id = request.POST.get("post-id")

            post = Post.objects.filter(id=post_id).first()
            if post and (post.author == request.user or has_group(request.user,'mod') or request.user.is_staff) :
                post.delete()
        if request.user.is_authenticated and "search-term" in request.POST:
            search_term = request.POST.get('search-term')
            posts = Post.objects.filter(tags__name__iregex = rf"{search_term}").filter(title__iregex= rf"{search_term}").order_by('created_at')
            limit = 5
            end = len(posts) if len(posts) <= limit else limit
            posts = posts[:end]
            # return render(request, 'main/posts_search.html',{"posts":posts})
        return redirect('/home')

    return render(request, 'main/home.html',{"posts":posts,"categories":categories})

@login_required(login_url='/login')
def search(request):
    if len(request.user.groups.filter(name='banned')):
        return HttpResponse(f"<h1>Your account ({request.user.username}) is Banned, please contact admin </h1>")
    search_term = request.POST.get("search-term")
    posts = Post.objects.all().order_by('created_at')
    # posts = [post for post in poststemp if search_term in post.title or search_term in tag.name for tag in post.tags.all ]
    # posts = Post.objects.filter(tags__name__iregex = rf"{search_term}").filter(title__iregex= rf"{search_term}").order_by('created_at')
    limit = 5
    end = len(posts) if len(posts) <= limit else limit
    posts = posts[:end]

    if request.POST:
        if request.user.is_authenticated and "post-id" in request.POST:
            post_id = request.POST.get("post-id")

            post = Post.objects.filter(id=post_id).first()
            if post and (post.author == request.user or has_group(request.user,'mod') or request.user.is_staff) :
                post.delete()
        return redirect('/home')

    return render(request, 'main/post_search.html',{"posts":posts})

    # post_category = Category.objects.get(id=id)
    # posts = Post.objects.filter(category = post_category).order_by('created_at')
    # categories = Category.objects.all()

    # if request.POST:
    #     post_id = request.POST.get("post-id")
    #     post = Post.objects.filter(id=post_id).first()
    #     if post and (post.author == request.user or has_group(request.user,'mod') or request.user.is_staff) :
    #         post.delete()

    # return render(request, 'main/posts_by_category.html',{"posts":posts,"categories":categories})

#======================================================================= USER

def login_user(request):
    print("login view used")
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if not has_group(user,'banned'):
            login(request, user)
        else:
            messages.success(request,("User Banned, please contact Admin"))
            redirect("/login")
    else:
        messages.success(request,("There was an error logging in, try again"))
        # Return an 'invalid login' error message.
        

def sign_up(request):
    if request.POST:
        form = RegisterationForm(request.POST)
        if form.is_valid():
            user = form.save()
            default.user_set.add(user)
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterationForm()
    
    return render(request, 'registration/sign_up.html', {'form':form})

#====================================================================== MOD
#=== Othermods
# @permission_required('user.add_user', login_url='/login')
def mod_menu(request):
    if has_group(request.user,'mod') or request.user.is_staff:

        return render(request, 'users/admin_panel.html')

    else: 
        return redirect('/home')

            # @staff_member_required(login_url='/login')
            # def sign_up_mod(request):
            #     if request.POST:
            #         form = RegisterationForm(request.POST)
            #         if form.is_valid():
            #             user = form.save()
            #             mod.user_set.add(user)
            #             return redirect('/home')
            #     else:
            #         form = RegisterationForm()
                
            #     return render(request, 'registration/sign_up.html', {'form':form})

#=== default Users
# @staff_member_required(login_url='/login')


# @permission_required('user.add_user', login_url='/login')
@login_required(login_url='/login')
def list_users(request):
    if has_group(request.user,'mod') or request.user.is_staff:
        User = get_user_model()
        users = User.objects.filter(groups__name='default')
        banned_users = User.objects.filter(groups__name='banned')
        moderators = User.objects.filter(groups__name='mod')

        if request.POST:
            user_id = request.POST.get("user-id")
            # user_id = None
            user_action = request.POST.get("user-action")
            user = User.objects.filter(id=user_id).first()
            print(f"user id = {user_id}")
            if user and (has_group(request.user,'mod') or request.user.is_staff) :
                group_default = Group.objects.get(name='default')
                group_banned = Group.objects.get(name='banned')
                group_mods = Group.objects.get(name='mod')
                if user_action == 'promote':
                    group_default.user_set.remove(user)
                    group_mods.user_set.add(user)
                if user_action == 'ban':
                        group_default.user_set.remove(user)
                        group_banned.user_set.add(user)
                if user_action == 'unban':
                        group_default.user_set.add(user)
                        group_banned.user_set.remove(user)                   
            # return render(request, 'users/list_users.html',{"users":users,"banned_users":banned_users})

        #         post.delete()

        return render(request, 'users/list_users.html',{"users":users,"banned_users":banned_users,"moderators":moderators})
    else: 
        return redirect('/home')

            # @staff_member_required(login_url='/login')
            # def user_crud(request):
            #     if request.method == 'POST':
            #         user_form = UpdateUserForm(request.POST, instance=request.user)

            #         if user_form.is_valid():
            #             user_form.save()
            #             return redirect('/home')
            #     else:
            #         user_form = UpdateUserForm(instance=request.user)

            #     return render(request, 'users/profile.html', {'user_form': user_form})


#====================================================================== POSTS
def post_description(request,id):
    if len(request.user.groups.filter(name='banned')):
        return HttpResponse(f"<h1>Your account ({request.user.username}) is Banned, please contact admin </h1>")
    valid_form = True
    form = CommentForm()
    post = Post.objects.get(id=id)
    if request.POST:
        if request.user.is_authenticated and "content" in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                parent_obj = None
                comment = form.save(commit=False)
                print("content = ", comment.content)

                try:
                    parent_id = int(request.POST.get('parent_id'))
                    print("parent id = ",parent_id)
                except:
                    parent_id = None

                if parent_id:
                    parent_obj = Comment.get_object(parent_id)
                    comment.parent = parent_obj
                comment.author = request.user
                comment.post = post
                comment.save()
            else:
                valid_form = False

        elif request.user.is_authenticated and "reaction_type" in request.POST:
            try:
                reaction = request.POST.get('reaction_type')
                print(f"reaction = {reaction}")
            except:
                reaction = None
            
            if reaction == 'Like':
                print("Like button pressed")
                post.like_button(request.user)
            if reaction == 'Dislike':
                print("Dislike button pressed")
                post.dislike_button(request.user)
            post.save()

        if valid_form:
            return redirect(post.get_show_url())

    comments = Comment.objects.filter(post=post)
    for comment in comments:
        replies =  Comment.objects.filter(parent=comment)
        if replies:
            comment.replies = replies
    
    return render(request, "posts/post_description.html",{"post":post,"comments":comments,"form":form})


def posts_by_category(request,id):
    if len(request.user.groups.filter(name='banned')):
        return HttpResponse(f"<h1>Your account ({request.user.username}) is Banned, please contact admin </h1>")
    post_category = Category.objects.get(id=id)
    posts = Post.objects.filter(category = post_category).order_by('created_at')
    categories = Category.objects.all()

    if request.user.is_authenticated and request.POST:
        post_id = request.POST.get("post-id")
        post = Post.objects.filter(id=post_id).first()
        if post and (post.author == request.user or has_group(request.user,'mod') or request.user.is_staff) :
            post.delete()

    return render(request, 'main/posts_by_category.html',{"posts":posts,"categories":categories})

@login_required(login_url='/login')
@permission_required("main.add_post", login_url="/login", raise_exception=False) #delete,update,view
def create_post(request):
    if len(request.user.groups.filter(name='banned')):
        return HttpResponse(f"<h1>Your account ({request.user.username}) is Banned, please contact admin </h1>")
    if request.POST:
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            if request.FILES:
                image = request.FILES["picture"]
                timestampe = time()
                image.name = f"{timestampe}{image.name}"
                post.picture = image

            post.save()
            form.save_m2m()
            return redirect('/home')
    else:
        form = PostForm()
        return render(request, 'posts/create_post.html',{"form":form})
    
def edit_post_view(request, id):  
    if len(request.user.groups.filter(name='banned')):
        return HttpResponse(f"<h1>Your account ({request.user.username}) is Banned, please contact admin </h1>")
    post = Post.get_object(id)
    if request.method == "POST":  
        form = PostForm(request.POST, instance=post)  
        if form.is_valid():  
                form.save() 
                return redirect(post.get_show_url()) 

    form = PostForm(instance=post)

    # categories = Category.get_all_bojects()  
    return render(request,'posts/posts_edit.html',{'form':form})  

def delete_post_view(request,id):
    Post.delete_object(id)
    return redirect("home")


    #====================================================================== CATEGORIES
def list_categories(request):
    if has_group(request.user,'mod') or request.user.is_staff:
        categories = Category.objects.all()


        return render(request, 'categories/list_categories.html',{"categories":categories})
    else: 
        return redirect('/home')

def category_description(request,id):
    category = Category.objects.get(id=id)
    return render(request, "categories/category_description.html",{"category":category})

@login_required(login_url='/login')
@permission_required("main.add_post", login_url="/login", raise_exception=False) #delete,update,view
def create_category(request):
    if request.POST:
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)

            category.save()
            return redirect('/list-categories') 
    else:
        form = CategoryForm()
        return render(request, 'categories/create_category.html',{"form":form})

@login_required(login_url='/login')
def edit_category_view(request, id):  
    category = Category.get_object(id)
    if request.method == "POST":  
        form = CategoryForm(request.POST, instance=category)  
        if form.is_valid():  
                form.save() 
                return redirect('/list-categories') 

    form = CategoryForm(instance=category)

    # categories = Category.get_all_bojects()  
    return render(request,'categories/categories_edit.html',{'form':form})  

@login_required(login_url='/login')
def delete_category_view(request,id):
    Category.delete_object(id)
    return redirect("/list-categories")

   #====================================================================== COMMENTS
def comment_description(request,id):
    if len(request.user.groups.filter(name='banned')):
        return HttpResponse(f"<h1>Your account ({request.user.username}) is Banned, please contact admin </h1>")
    comment = Comment.get_object(id)
    replies = Comment.objects.filter(parent=comment)
    return render(request, "comments/comment_description.html",{"comment":comment,'replies':replies})

@login_required(login_url='/login')
def like_comment(request,id):
    if len(request.user.groups.filter(name='banned')):
        return HttpResponse(f"<h1>Your account ({request.user.username}) is Banned, please contact admin </h1>")
    signed_in = request.user
    comment = Comment.get_object(id)
    post = comment.post

    if signed_in and comment:
        try:
            comment.likes.remove(signed_in)
        except:
            comment.likes.add(signed_in)

    return post_description(request, post.id)
       

@login_required(login_url='/login')
def create_comment(request):
    if len(request.user.groups.filter(name='banned')):
        return HttpResponse(f"<h1>Your account ({request.user.username}) is Banned, please contact admin </h1>")
    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment['author'] = request.user
            comment.save()
            return redirect(comment.get_post_url()) 
    else:
        form = CommentForm()
        return render(request, 'comments/create_comment.html',{"form":form})

@login_required(login_url='/login')   
def edit_comment_view(request, id): 
    if len(request.user.groups.filter(name='banned')):
        return HttpResponse(f"<h1>Your account ({request.user.username}) is Banned, please contact admin </h1>") 
    comment = Comment.get_object(id)
    if request.method == "POST":  
        form = CommentForm(request.POST, instance=comment)  
        if form.is_valid():  
                comment = form.save()
                return redirect(comment.get_post_url()) 

    form = CommentForm(instance=comment)

    # categories = Category.get_all_bojects()  
    return render(request,'comments/comments_edit.html',{'form':form})  

@login_required(login_url='/login')
def delete_comment_view(request,id):
    comment = Comment.get_object(id)
    post_url = comment.get_post_url()
    Comment.delete_object(id)
    return redirect(post_url)


    #====================================================================== FORBIDDENS

    #     path('list-forbiddens',views.list_forbiddens,name='list_forbiddens'),
    # path('forbidden/create',views.create_forbidden,name='create_forbidden'),
    # path('forbidden/<int:id>/description',views.forbidden_description,name='forbidden.description'),
    # path("forbidden/<int:id>/edit", views.edit_forbidden_view, name='forbidden.edit'),
    # path("forbidden/<int:id>/delete", views.delete_forbidden_view, name='forbidden.delete'),
@login_required(login_url='/login')
def list_forbiddens(request):
    if has_group(request.user,'mod') or request.user.is_staff:
        forbiddens = Forbidden.objects.all()

        return render(request, 'forbiddens/list_forbiddens.html',{"forbiddens":forbiddens})
    else: 
        return redirect('/home')

def forbidden_description(request,id):
    forbidden = Forbidden.objects.get(id=id)
    return render(request, "forbiddens/forbidden_description.html",{"forbidden":forbidden})

@login_required(login_url='/login')
@permission_required("main.add_post", login_url="/login", raise_exception=False) #delete,update,view
def create_forbidden(request):
    if request.POST:
        form = ForbiddenForm(request.POST)
        if form.is_valid():
            forbidden = form.save(commit=False)

            forbidden.save()
            return redirect('/list-forbiddens')
    else:
        form = ForbiddenForm()
        return render(request, 'forbiddens/create_forbidden.html',{"form":form})
    
def edit_forbidden_view(request, id):  
    forbidden = Forbidden.get_object(id)
    if request.method == "POST":  
        form = ForbiddenForm(request.POST, instance=forbidden)  
        if form.is_valid():  
                form.save() 
                return redirect('/list-forbiddens') 

    form = ForbiddenForm(instance=forbidden)

    return render(request,'forbiddens/forbiddens_edit.html',{'form':form})  

def delete_forbidden_view(request,id):
    Forbidden.delete_object(id)
    return redirect("/list-forbiddens")


   #====================================================================== TAGS
   
def list_tags(request):
    if len(request.user.groups.filter(name='banned')):
        return HttpResponse(f"<h1>Your account ({request.user.username}) is Banned, please contact admin </h1>")
        tags = Tag.objects.all()
        return render(request, 'tags/list_tags.html',{"tags":tags})

def tag_description(request,id):
    if len(request.user.groups.filter(name='banned')):
        return HttpResponse(f"<h1>Your account ({request.user.username}) is Banned, please contact admin </h1>")
    tag = Tag.objects.get(id=id)
    return render(request, "tags/tag_description.html",{"tag":tag})

@login_required(login_url='/login')
def create_tag(request):
    if len(request.user.groups.filter(name='banned')):
        return HttpResponse(f"<h1>Your account ({request.user.username}) is Banned, please contact admin </h1>")
    if request.POST:
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            tag.save()
            return redirect('/list-tags') 
    else:
        form = TagForm()
        return render(request, 'tags/create_tag.html',{"form":form})

@permission_required("main.add_post", login_url="/login", raise_exception=False) #delete,update,view 
def edit_tag_view(request, id):  
    tag = Tag.get_object(id)
    if request.method == "POST":  
        form = TagForm(request.POST, instance=tag)  
        if form.is_valid(): 
            tag = form.save() 
            tag.save()
        return redirect('/list-tags') 

    form = TagForm(instance=tag)

    # categories = Category.get_all_bojects()  
    return render(request,'tags/tags_edit.html',{'form':form})  

@permission_required("main.add_post", login_url="/login", raise_exception=False) #delete,update,view
def delete_tag_view(request,id):
    Tag.delete_object(id)
    return redirect("/list-tags")

