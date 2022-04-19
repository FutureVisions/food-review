from multiprocessing import context
from pdb import post_mortem
from re import template
from urllib import request
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# renders the login reg page
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

# renders the dashboard page
def dashboard(request):
    context = {
        'user': User.objects.get(id=request.session['log_user_id']),
        'one_user': User.objects.all(),
        'all_food': Food.objects.all(),
        'comment': Comment.objects.all()
    }
    return render(request, 'dashboard.html', context)

# renders the specific user acc page
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

# renders the specific food page
def food(request, food_id):
    if "log_user_id" not in request.session:
        return redirect('/')
    else:
        context = {
            'current_user' : User.objects.get(id=request.session['log_user_id']),
            'food_product': Food.objects.get(id=food_id),
            'users_comment': Comment.objects.all(),
            'all_food': Food.objects.all(),
            'all_likes': Food.objects.get(id=food_id).likes.all()
        }
        return render(request, 'food.html', context)

def add_comment(request, food_id):
    if "log_user_id" not in request.session:
        return redirect('/')
    else:
        current_user = User.objects.get(id=request.session['log_user_id'])
        food_item = Food.objects.get(id=food_id)
        adding_comment = Comment.objects.create(content = request.POST['content'], post=food_item, uploaded_by = current_user)
        return redirect(f'/food/{food_id}')

def delete_comment(request,food_id, comment_id):
    if "log_user_id" not in request.session:
        return redirect('/')
    else:
        current_user = User.objects.get(id=request.session['log_user_id'])
        food_item = Food.objects.get(id=food_id)
        comment_to_delete = Comment.objects.get(id=comment_id)
        comment_to_delete.delete()
        return redirect(f'/food/{food_id}')


def like(request, food_id):
    if "log_user_id" not in request.session:
        return redirect('/')
    else:
        current_food = Food.objects.get(id=food_id)
        current_user = User.objects.get(id=request.session['log_user_id'])
        current_food.likes.add(current_user)
        return redirect(f'/food/{food_id}')

def unlike(request, food_id):
    if "log_user_id" not in request.session:
        return redirect('/')
    else:
        current_food = Food.objects.get(id=food_id)
        current_user = User.objects.get(id=request.session['log_user_id'])
        current_food.likes.remove(current_user)
        return redirect(f'/food/{food_id}')


