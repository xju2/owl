from django.shortcuts import render, get_object_or_404, render_to_response
from app.movie.models import Movie
import random
random.seed = 20

def index(request):
<<<<<<< HEAD
    print(request.session.get("_auth_user_id"))
    user_id = request.session.get('_auth_user_id')
    if user_id:
        try:
            user = OwlUser.objects.get(user_id=user_id)
            ctx = dict(user=user, top10_movies=Movie.objects.top_10())
            return render(request, 'movie/index.html', ctx)
        except OwlUser.DoesNotExist:
            message = "User: "+str(user_id)+" does not exist"
    else:
        message = "What's user_name? "
    ctx = dict(message=message, retry_url="index")
    return render_to_response('error.html', ctx)


def new_user(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['password']
    user = OwlUser.objects.create_user(index=random.random() * 10000, name=username)
    user.password = password
    user.last_name = last_name
    user.first_name = first_name
    user.email = email
    user.save()
    context = {'user': user}
    return render(request, 'movie/index.html', context)

=======
    ctx = dict(user=request.user, top10_movies=Movie.objects.top_10())
    return render(request, 'movie/index.html', ctx)
>>>>>>> ycz

def detail(request, movie_id):
    ctx = dict(user=request.user)
    movie = get_object_or_404(Movie, pk=movie_id)
    ctx.update(dict(movie=movie))
    return render(request, 'movie/detail.html', ctx)
