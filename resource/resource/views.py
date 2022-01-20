from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.http import HttpResponse
import os
from django.contrib.auth import authenticate, login, logout

from user_view.models import Member

def home(request):
    return render(request, 'home.html')

def userLogout(request):
    logout(request)
    return redirect('/')


def userLogin(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_ob = User.objects.filter(username=username).first()
        print(user_ob)

        if user_ob is None:
            msg = {'msg': 'User does not exist'}
            print(msg)
            return render(request, 'login_register.html', { "msg": msg, "page": page })

        user = authenticate(username=username, password=password)
        print(user)
        if user is None:
            msg = {'msg': 'Invalid Credentials'}
            print(msg)
            return render(request,'login_register.html', {'msg': msg, "page": page})

        login(request, user)
        return redirect('/')
    return render(request, 'login_register.html', {'page': page})


def userRegister(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        if User.objects.filter(email=email).first() is not None:
            msg = {'msg': 'Email already exists'}
            print(msg)
            return render(request, 'login_register.html', {'msg2': msg, "page": "register"})
        elif User.objects.filter(username=username).first() is not None:
            msg = {'msg': 'Username already exists'}
            print(msg)
            return render(request, 'login_register.html', {'msg2': msg, "page": "register"})
        else:
            user_ob = User.objects.create(
                username=username, email=email, first_name=first_name, last_name=last_name)
            user_ob.set_password(password)
            user_ob.save()
            login(request, user_ob)
            member=Member.objects.create(usn=username,first_name=first_name,last_name=last_name,email=email)
            member.save()
            return redirect('/')
    return render(request, 'login_register.html', {'page': "register"})
