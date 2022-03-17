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
    }
    return render(request, 'account.html', context)
