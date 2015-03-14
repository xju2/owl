__author__ = 'xju'

from django.core.management.base import BaseCommand
from app.movie.models import Movie


class Command(BaseCommand):
    args = ""
    help = "Update Movie's rated users"

    def handle(self, *args, **options):
        for movie in Movie.objects.all():
            # movie.rated_users = movie.realrate_set.all().count()
            movie.rated_users = movie.phantomrate_set.all().count()
            movie.save()
        self.stdout.write("Successfully updated movie's rated users")
