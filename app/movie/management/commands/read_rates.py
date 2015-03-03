# -*- coding: utf_8 -*-
from django.core.management.base import BaseCommand, CommandError
from app.movie.models import PhantomUser
from app.movie.models import Movie
from app.movie.models import PhantomRate


from itertools import islice
import time


class Command(BaseCommand):
    args = "<file>"
    help = "Add Users from a text file"

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('No input file given')
        n = 10000
        n_comments = 0
        rate_list = args[0]
        start_time = time.time()
        with open(rate_list) as f:
            while True:
                next_n_lines = list(islice(f, n))
                if not next_n_lines:
                    break
                for line in next_n_lines:
                    n_comments += 1
                    user_id, movie_id, rate = line.split()
                    rate = float(rate)
                    try:
                        user = PhantomUser.objects.get(inner_id=user_id)
                        user.watched_movies += 1
                    except PhantomUser.DoesNotExist:
                        self.stderr.write("User %s does not exist" % user_id)
                        continue
                    try: 
                        movie = Movie.objects.get(inner_id=movie_id)
                        movie.rated_users += 1
                    except Movie.DoesNotExist:
                        self.stderr.write("Movie %s does not exist" % movie_id)
                        continue
                    user.save()
                    movie.save()
                    q = PhantomRate(id=None, user=user, movie=movie, rate=rate)
                    q.save()
        self.stdout.write('Successfully added %d rates' % n_comments)
        self.stdout.write('time takes: %s seconds' % (time.time()-start_time))
