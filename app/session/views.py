# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def login_view(request):
    ph_nickname = "Nick name or Email"
    ph_password = "Password"

    ctx = {
            'ph_nickname':ph_nickname,
            'ph_password':ph_password,
    }

    try:
        username = request.POST['inputNickname']
        password = request.POST['inputPassword']
    except:
        username = ""
        password = ""
        return render(request, 'session/login.html',ctx)
    
    if not User.objects.filter(username=username).exists():
        ph_nickname = "No matched User!"
    else:
        user = authenticate(username = username, password=password)
        if user == None:
            ph_password = "Wrong Password!"
        else:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect(request.GET.get('next','/'))
    ctx = {
            'ph_nickname':ph_nickname,
            'ph_password':ph_password,
    }

    return render(request, 'session/login.html',ctx)

def user_logout(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect("/")


def register_view(request):

    ph_nickname = "Nick name"
    ph_email = "Email address"
    ph_password = "Password"
    ph_repassword = "Retype Password"

    ctx = {
            'ph_nickname':ph_nickname,
            'ph_email':ph_email,
            'ph_password':ph_password,
            'ph_repassword':ph_repassword,
    }

    try:
        username = request.POST['inputNickname']
        email = request.POST['inputEmail']
        password = request.POST['inputPassword']
        repassword = request.POST['inputRePassword']
    except:
        username = ""
        email = ""
        password = ""
        return render(request, 'session/register.html',ctx)
    
    check_username = True
    check_email = True
    check_password = True

    if len(username)<3:
        ph_nickname = "Nickname is too short!"
        check_username = False
    if User.objects.filter(username=username).exists():
        ph_nickname = "Duplicated Nickname!"
        check_username = False
    if len(email)<8:
        ph_email = "Wrong Email Format!"
        check_email = False
    if User.objects.filter(email=email).exists():
        ph_email = "Duplicated Email!"
        check_email = False

    if len(password)<8:
        ph_password = "Password is too short!"
        check_password = False
    if password!=repassword:
        ph_repassword = "Password not matched!"
        check_password = False

    ctx = {
            'ph_nickname':ph_nickname,
            'ph_email':ph_email,
            'ph_password':ph_password,
            'ph_repassword':ph_repassword,
    }

    if check_username and check_email and check_password:
        user = User.objects.create_user(
                username = username,
                email = email,
                password = password)
        user.save()
        user = authenticate(username = username, password=password)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'session/register.html',ctx)
    

def home(request):
    context = RequestContext(request,
            {'user': request.user})
    return render_to_response('session/home.html',
            context_instance=context)
