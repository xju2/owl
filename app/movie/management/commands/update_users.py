__author__ = 'xju'

from django.core.management.base import BaseCommand
from app.movie.models import PhantomUser


class Command(BaseCommand):
    args = ""
    help = "Update User's watched movies "

    def handle(self, *args, **options):
        print("phantom users: ", PhantomUser.objects.all().count())
        for user in PhantomUser.objects.all():
            # user.watched_movies = user.realrate_set.all().count()
            user.watched_movies = user.phantomrate_set.all().count()
            user.save()
        self.stdout.write("Successfully updated user's watched movies")
