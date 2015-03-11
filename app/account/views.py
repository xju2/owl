#encoding=utf8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from string import Template

from owl.settings import LOGIN_URL

from app.account.forms import *

def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = SignInForm()
    ctx = {'form': form}
    ctx.update(csrf(request))
    return render_to_response('account/sign_in.html', ctx)


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = SignUpForm()
    ctx = {'form': form}
    ctx.update(csrf(request))
    return render_to_response('account/sign_up.html', ctx)


<<<<<<< HEAD
def do_sign_up(request):
    post = request.POST.dict()
    post["password"] = User.objects.make_random_password()
    del post["csrfmiddlewaretoken"]
    user = User.objects.create_user(**post)
    try:

        user.save()
        user.email_user('Owl Password', Template('Username: $username, Password: $password').substitute(**post),
                        "oppps@163.com")
        q = OwlUser(id=None, user=user, watched_movies=0)
        q.save()
    except:
        print("User not created!")
        pass
=======
def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if type(request.user) == User:
            form.set_email(request.user.email)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            d = {'username': user.username, 'password': password}
            user.email_user('ChinaDaaS平台密码重置', \
                            Template('username: $username, new password: $password').substitute(**d), "oppps@163.com")
            return HttpResponseRedirect('/')
    else:
        form = ResetPasswordForm()
    ctx = {'form': form, 'user': request.user}
    ctx.update(csrf(request))
    return render_to_response('account/reset_password.html', ctx)
>>>>>>> ycz


@login_required
<<<<<<< HEAD
def change_pwd(request):
    print("change pwd", request.user)
    ctx = dict(user=request.user)
=======
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']
            user = request.user
            user.last_name = last_name
            user.first_name = first_name
            user.save()
            return HttpResponseRedirect('/')
    else:
        form = ProfileForm()
    ctx = {'form': form, 'user': request.user}
>>>>>>> ycz
    ctx.update(csrf(request))
    return render_to_response('account/profile.html', ctx)


@login_required
def security(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        username = request.user.username
        form.set_user(username)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = User.objects.get_by_natural_key(username)
            user.set_password(password)
            user.save()
            return HttpResponseRedirect(LOGIN_URL)
    else:
        form = ChangePasswordForm()
    ctx = {'form': form, 'user': request.user}
    ctx.update(csrf(request))
    return render_to_response('account/security.html', ctx)


def sign_out(request):
    logout(request)
    return HttpResponseRedirect('/')

