# from django.shortcuts import render

# from time import time

# from .forms import RegisterationForm, UpdateUserForm
# from .admin import mod, default
# # from.templatetags.has_group import has_group

# from django import template
# from django.contrib.auth import get_user_model
# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required, permission_required
# from django.contrib.admin.views.decorators import staff_member_required
# from django.contrib.auth import login, logout, authenticate

# # Create your views here.
# @staff_member_required(login_url='/login')
# def list_users(request):

#     User = get_user_model()
#     users = User.objects.all()

#     # if request.POST:
#     #     user_id = request.POST.get("user-id")
#     #     user = User.objects.filter(id=user_id).first()
#     #     if user and (has_group(request.user,'mod') or request.user.is_staff) :
#     #         post.delete()

#     return render(request, 'users/list_users.html',{"users":users})

# def sign_up(request):
#     if request.POST:
#         form = RegisterationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             default.user_set.add(user)
#             login(request, user)
#             return redirect('/home')
#     else:
#         form = RegisterationForm()
    
#     return render(request, 'registration/sign_up.html', {'form':form})