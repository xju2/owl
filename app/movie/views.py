from django.shortcuts import render, get_object_or_404
from app.movie.models import Movie
from app.movie.services import train_user
import random
random.seed = 20


def index(request):
    suggest_movie_id = train_user(request.user)
    top10_suggest = Movie.objects.filter(id__in=suggest_movie_id)
    ctx = dict(user=request.user, top10_movies=Movie.objects.top_10(), suggest=top10_suggest)
    return render(request, 'movie/index.html', ctx)


def detail(request, movie_id):
    ctx = dict(user=request.user)
    movie = get_object_or_404(Movie, pk=movie_id)
    ctx.update(dict(movie=movie))
    return render(request, 'movie/detail.html', ctx)
