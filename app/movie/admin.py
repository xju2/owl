from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from app.movie.models import Movie
from app.movie.models import RealRate
from app.movie.models import SuggestRate
from app.movie.models import OwlUser

class ActiveUserListFilter(admin.SimpleListFilter):
    title = _('active users')
    parameter_name = 'user'

    def lookups(self, request, model_admin):

        return (
            ('50', _('rated 50 movies')),
            ('25', _('rated 25 movies')),
        )

    def queryset(self, request, queryset):
        try:
            n_movies = int(self.value())
            return queryset.filter(watched_movies__gt=n_movies)
        except TypeError:
            return None

class RealRateAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'rate']
    ordering = ['user']

class UserAdmin(admin.ModelAdmin):
    list_filter = (ActiveUserListFilter,)

admin.site.register(Movie)
admin.site.register(SuggestRate)
admin.site.register(RealRate, RealRateAdmin)
admin.site.register(OwlUser)
