from django.contrib import admin

# Register your models here.

from .models import Genre, Movie, Review, Cluster

class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('movie', 'rating', 'user_name', 'comment', 'pub_date')
    list_filter = ['pub_date', 'user_name']
    # list_display = ('movie', 'rating', 'user', 'comment', 'pub_date')
    # list_filter = ['pub_date', 'user']
    search_fields = ['comment']


class ClusterAdmin(admin.ModelAdmin):
    model = Cluster
    list_display = ['name', 'get_members']


class MovieAdmin(admin.ModelAdmin):
    model = Movie
    list_display = ['name', 'duration', 'get_genres']


admin.site.register(Genre)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Cluster, ClusterAdmin)