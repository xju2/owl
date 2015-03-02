__author__ = 'xju'

from django.core.management.base import BaseCommand
from app.movie.models import User


class Command(BaseCommand):
    args = ""
    help = "Update User's watched movies "

    def handle(self, *args, **options):
        for user in User.objects.all():
            user.watched_movies = user.realrate_set.all().count()
            user.save()
        self.stdout.write("Successfully updated user's watched movies")
