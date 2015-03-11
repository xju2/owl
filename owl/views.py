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


def index(request):
    ctx = dict(user=request.user)
    return render_to_response('index.html', ctx)


def about(request):
    ctx = dict(user=request.user)
    return render_to_response('about.html', ctx)

