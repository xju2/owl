from django.shortcuts import render, get_object_or_404, render_to_response
from app.movie.models import Movie
import random
random.seed = 20


def index(request):
    ctx = dict(user=request.user, top10_movies=Movie.objects.top_10())
    return render(request, 'movie/index.html', ctx)


def detail(request, movie_id):
    ctx = dict(user=request.user)
    movie = get_object_or_404(Movie, pk=movie_id)
    ctx.update(dict(movie=movie))
    return render(request, 'movie/detail.html', ctx)
