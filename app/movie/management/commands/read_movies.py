from django.core.management.base import BaseCommand, CommandError
from app.movie.models import Movie

# -*- coding: utf_8 -*-
from itertools import islice


class Command(BaseCommand):
    args = '<file>'
    help = 'Add movies from a text file'

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('No input file given')
        movie_list = args[0]
        n = 10000
        counter = 0
        with open(movie_list) as f:
            while True:
                next_n_lines = list(islice(f,n))
                if not next_n_lines:
                    break
                for line in next_n_lines:
                    all_items = line.split()
                    index = all_items[0]
                    name = all_items[1]
                    try:
                        Movie.objects.get(index=index)
                    except Movie.DoesNotExist:
                        q = Movie.objects.create_movie(index, name)
                        q.save()
                    counter += 1
        self.stdout.write('Successfully added %d movies' % counter)
