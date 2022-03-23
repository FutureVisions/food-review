from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def home(request):
    return render(request, 'index.html',)

def home_create(request):
    errors = User.objects.basic_validator(request.POST, request.FILES)
    user= User.objects.filter(email=request.POST['email'])
    if user:
        messages.error(request, "Email is already taken!")
        return redirect('/')
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user=User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        pfp = request.FILES['pfp'],
        password=pw_hash)
        request.session['log_user_id'] = new_user.id
    return redirect('/dashboard')

def log_user(request):
    user= User.objects.filter(email=request.POST['email'])
    if user:
        logged_user= user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['log_user_id'] = logged_user.id
            return redirect('/dashboard')
        else:
            messages.error(request, 'Invalid Email or Password!', extra_tags='invalid')
            return redirect('/')
    messages.error(request, "Email does not exist")
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    context = {
        'user': User.objects.get(id=request.session['log_user_id']),
        'one_user': User.objects.all(),
        'all_food': Food.objects.all()
    }
    return render(request, 'dashboard.html', context)

def account(request, user_id):
    if "log_user_id" not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['log_user_id']),
        "account_user": User.objects.get(id=user_id),
        "food_objects": Food.objects.all(),
        "uploaded_food":User.objects.get(id=user_id).users_food.all(),
    }
    return render(request, 'account.html', context)


def add_food(request):
    if "log_user_id" not in request.session:
        return redirect('/')
    else:
        current_user = User.objects.get(id=request.session['log_user_id'])
        food_review = {
            Food.objects.create(
                title = request.POST['title'],
                food_image = request.FILES['food_image'],
                food_uploader = current_user
            )
        }
    return redirect('/dashboard')

def food(request, food_id):
    if "log_user_id" not in request.session:
        return redirect('/')
    else:
        context = {
            'current_user' : User.objects.get(id=request.session['log_user_id']),
            'food_product': Food.objects.get(id=food_id),
            'users_comment': Comment.objects.all(),
        }
        return render(request, 'food.html', context)

def add_comment(request):
    if "log_user_id" not in request.session:
        return redirect('/')
    else:
        current_user = User.objects.get(id=request.session['log_user_id'])
        adding_comment = Comment.objects.create(content = request.POST['added_comment'], posted_by=current_user)
        return redirect('/')

def delete_comment(request, comment_id):
    if "log_user_id" not in request.session:
        return redirect('/')
    else:
        comment_to_delete = Comment.objects.get(id=comment_id)
        comment_to_delete.delete()
        return redirect('/food')