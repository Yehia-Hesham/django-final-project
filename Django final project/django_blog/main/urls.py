from django.urls import path
from . import views

urlpatterns = [
    path("",views.home, name='home'),
    path("home",views.home, name='home'),
    path("moderation-menu",views.mod_menu, name='mod_menu'),
    path("list-users",views.list_users, name='list_users'),
    path('sign-up',views.sign_up, name='sign_up'),
    path('login',views.login_user, name='login'),
    # path('sign-up-mod',views.sign_up_mod, name='sign_up_mod'),


    path('post/create',views.create_post,name='create_post'),
    path('post/<int:id>/description',views.post_description,name='post.description'),
    path("post/<int:id>/edit", views.edit_post_view, name='post.edit'),
    path("post/<int:id>/delete", views.delete_post_view, name='post.delete'),
    path("post/<int:id>/category", views.posts_by_category, name='post.category'),
    path("search", views.search, name='post.search'),
    
    path('list-categories',views.list_categories,name='list_categories'),
    path('category/create',views.create_category,name='create_category'),
    path('category/<int:id>/description',views.category_description,name='category.description'),
    path("category/<int:id>/edit", views.edit_category_view, name='category.edit'),
    path("category/<int:id>/delete", views.delete_category_view, name='category.delete'),

    path('comment/create',views.create_comment,name='create_comment'),
    path('comment/<int:id>/description',views.comment_description,name='comment.description'),
    path("comment/<int:id>/edit", views.edit_comment_view, name='comment.edit'),
    path("comment/<int:id>/delete", views.delete_comment_view, name='comment.delete'),
    path("comment/<int:id>/like", views.like_comment, name='comment.like'),

    path('list-forbiddens',views.list_forbiddens,name='list_forbiddens'),
    path('forbidden/create',views.create_forbidden,name='create_forbidden'),
    path('forbidden/<int:id>/description',views.forbidden_description,name='forbidden.description'),
    path("forbidden/<int:id>/edit", views.edit_forbidden_view, name='forbidden.edit'),
    path("forbidden/<int:id>/delete", views.delete_forbidden_view, name='forbidden.delete'),

    path('list-tags',views.list_tags,name='list_tags'),
    path('tag/create',views.create_tag,name='create_tag'),
    path('tag/<int:id>/description',views.tag_description,name='tag.description'),
    path("tag/<int:id>/edit", views.edit_tag_view, name='tag.edit'),
    path("tag/<int:id>/delete", views.delete_tag_view, name='tag.delete'),
]