#encoding=utf8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

import time
import hashlib


def index(request):
    ctx = dict(username=request.session.get('username'))
    return render_to_response('account/index.html', ctx)


def tologin(request):
    #request.session['prepath'] = request.META.get('HTTP_REFERER')
    ctx = dict(username=request.session.get('username'))
    if ctx.get('username') and ctx.get('email') and ctx.get('timestamp'):
        return HttpResponseRedirect('account/index/')
    return render_to_response('account/login.html', ctx)


def tosignup(request):
    #request.session['prepath'] = request.META.get('HTTP_REFERER')
    ctx = dict(username=request.session.get('username'))
    if ctx.get('username') and ctx.get('email') and ctx.get('timestamp'):
        return HttpResponseRedirect('movie/index/')
    return render_to_response('account/signup.html', ctx)


def login(request):
    email = request.POST.get('email')
    passwd = request.POST.get('passwd')
    p = PersonService().login_auth(email, passwd)
    ctx = dict(username=request.session.get('username'))
    if p:
        if not passwd:
            passwd = None
        else:
            passwd = hashlib.md5(passwd).hexdigest()
        if (passwd or p.passwd) and passwd != p.passwd:
            ctx.update(dict(message='登录失败，原因：密码不正确'))
            ctx.update(dict(retry_url='account/tologin/'))
            return render_to_response('error.html', ctx)
        request.session['username'] = p.name
        request.session['email'] = p.email
        request.session['timestamp'] = long(time.time())
    else:
        ctx.update(dict(message='登录失败，原因：用户不存在'))
        ctx.update(dict(retry_url='account/tologin/'))
        return render_to_response('error.html', ctx)
    prepath = request.session['prepath']
    del request.session['prepath']
    return HttpResponseRedirect('/index/')


def to_change_pwd(request):
    request.session['prepath'] = request.META.get('HTTP_REFERER')
    ctx = dict(username=request.session.get('username'))
    if ctx.get('username') and ctx.get('email') and ctx.get('timestamp'):
        return render_to_response('account/changepwd.html', ctx)
    return HttpResponseRedirect('acount/tologin/')


def change_pwd(request):
    old_pwd = request.POST.get('oldpasswd')
    new_pwd = request.POST.get('newpasswd')
    p = PersonService().current(request)
    ctx = dict(username=request.session.get('username'))
    if not old_pwd:
        old_pwd = None
    else:
        old_pwd = hashlib.md5(old_pwd).hexdigest()
    if not new_pwd:
        new_pwd = None
    else:
        new_pwd = hashlib.md5(new_pwd).hexdigest()
    if p:
        if (old_pwd or p.passwd) and old_pwd != p.passwd:
            ctx.update(dict(message='修改密码失败，原因：旧密码不正确'))
            ctx.update(dict(retry_url='account/tochangepwd/'))
            return render_to_response('error.html', ctx)
        p.passwd = new_pwd
        p.save()
    else:
        ctx.update(dict(message='修改密码失败，原因：请先登录系统'))
        ctx.update(dict(retry_url='account/tologin/'))
        return render_to_response('error.html', ctx)
    prepath = request.session['prepath']
    del request.session['prepath']
    ctx.update(dict(message='已成功修改密码'))
    return render_to_response('account/success.html', ctx)


def logout(request):
    prepath = request.META.get('HTTP_REFERER')
    if request.session.get('username'):
        del request.session['username']
    return HttpResponseRedirect('account/index/')

