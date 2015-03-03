from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class MovieManager(models.Manager):
    def create_movie(self, index, name):
        movie = self.create(inner_id=index, name=name)
        return movie


class Movie(models.Model):
    inner_id = models.PositiveIntegerField()
    name = models.CharField(max_length=25)
    avg_rate_site = models.SmallIntegerField(null=True)  # convert decimal value to integer
    #publish_date = models.DateTimeField('date released', default=timezone.now(), null=True)
    publish_date = models.CharField('date released', max_length=11, default="NLL", null=True)
    types = models.CharField(max_length=40, null=True)
    rated_users = models.PositiveIntegerField(default=0, blank=True, null=True)
    publish_country = models.CharField(max_length=50, null=True)
    language = models.CharField(max_length=50, null=True)  # use Chinese or English?
    directors = models.CharField(max_length=50, null=True)
    actors = models.CharField(max_length=400, null=True)
    length = models.CharField(max_length=20, default="NA", null=True)

    objects = MovieManager()

    def __str__(self):
        return self.name

    def avg_rate(self):
        total_rate = 0
        n_rate = 0
        for real_rate in self.realrate_set.all():
            total_rate += real_rate.rate
            n_rate += 1
        return total_rate * 1.0 / n_rate


class OwlUserManager(models.Manager):
    def create_user(self, index, name):
        user = self.create(inner_id=index, username=name)
        return user


class OwlUser(User):
    inner_id = models.PositiveIntegerField()
    watched_movies = models.PositiveSmallIntegerField(default=0)

    objects = OwlUserManager()

    def top_suggest(self):
        return self.suggestrate_set.order_by('rate')[:10]

    def __str__(self):
        return self.name


class RateBaseManager(models.Manager):
    def order_by_rate(self):
        return self.order_by('rate').reverse()

    def favored_movies(self):
        return self.filter(rate__gt=5.0)

    def top_10(self):
        return self.order_by('rate').reverse()[:10]


class RateBase(models.Model):
    user = models.ForeignKey(OwlUser, related_name="%(app_label)s_%(class)s_related")
    movie = models.ForeignKey(Movie, related_name="%(app_label)s_%(class)s_related")
    rate = models.SmallIntegerField()
    objects = RateBaseManager()

    def __str__(self):
        return self.user.name, " rated ", self.movie.name, " as ", self.rate

    class Meta:
        abstract = True
        # ordering = ['rate']


class RealRate(RateBase):
    from_site = models.CharField(max_length=30)


class SuggestRate(RateBase):
    pass

