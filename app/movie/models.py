from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class MovieManager(models.Manager):
    def create_movie(self, index, name):
        movie = self.create(id=index, name=name)
        return movie

    def top_10(self):
        return self.order_by('avg_rate_site').reverse()[:10]


class Movie(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=25)
    avg_rate_site = models.SmallIntegerField(null=True)  # convert decimal value to integer
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

    def avg_rate_ph(self):
        total_rate = 0
        n_rate = 0
        for real_rate in self.phantomrate_set.all():
            total_rate += real_rate.rate
            n_rate += 1
        return total_rate * 1.0 / n_rate

    def get_ars(self):
        return self.avg_rate_site/100.0




class RateBaseManager(models.Manager):

    def order_by_rate(self):
        return self.order_by('rate').reverse()

    def favored_movies(self):
        return self.filter(rate__gt=5.0)

    def top_10(self):
        return self.order_by('rate').reverse()[:10]


class RateBase(models.Model):
    user = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_related")
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


class PhantomUser(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    watched_movies = models.PositiveSmallIntegerField(default=0)


class PhantomRate(models.Model):
    user = models.ForeignKey(PhantomUser)
    movie = models.ForeignKey(Movie)
    rate = models.SmallIntegerField()

    def __str__(self):
        return self.user.inner_id, " rated ", self.movie.name, " as ", self.rate
