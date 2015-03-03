from django.shortcuts import render, get_object_or_404
from app.movie.models import Movie, User
import random
random.seed = 20

def login(request):
    return render(request, 'movie/login.html')

def index(request):
    ctx = dict(username=request.session.get('username'))
    return render(request, 'movie/index.html', ctx)

def new_user(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['password']
    user = User.objects.create_user(index=random.random() * 10000, name=username)
    user.password = password
    user.last_name = last_name
    user.first_name = first_name
    user.email = email
    user.save()
    context = {'user': user}
    return render(request, 'movie/index.html', context)

def detail(request, movie_id):
    ctx = dict(username=request.session.get('username'))
    movie = get_object_or_404(Movie, pk=movie_id)
    ctx.update(dict(movie=movie))
    return render(request, 'movie/detail.html', ctx)
