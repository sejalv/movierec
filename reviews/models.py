from django.db import models
from django.contrib.auth.models import User
import numpy as np


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=200)
    # year = models.IntegerField()
    duration = models.CharField(max_length=10)
    genres = models.ManyToManyField(Genre)

    def average_rating(self):
        all_ratings = map(lambda x: x.rating, self.review_set.all())
        return np.mean(all_ratings)

    def get_genres(self):
        return "\n".join([u.name for u in self.genres.all()])
        
    def __unicode__(self):
        return self.name


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (1.5, '1.5'),
        (2, '2'),
        (2.5, '2.5'),
        (3, '3'),
        (3.5, '3.5'),
        (4, '4'),
        (4.5, '4.5'),
        (5, '5'),
    )
    movie = models.ForeignKey(Movie)
    pub_date = models.DateTimeField('date published')
    #user_name = models.CharField(max_length=100)
    user_name = models.ForeignKey(User, to_field='username')
    comment = models.CharField(max_length=200, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, choices=RATING_CHOICES)


class Cluster(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def get_members(self):
        return "\n".join([u.username for u in self.users.all()])


    ''' for recos based genre+movie prefs
class UserPreferences(models.Model):
    user = models.ForeignKey(User)
    genre_pref = models.ManyToManyField(Genre)
    movie_pref = models.ManyToManyField(Movie)
    # review = models.ManyToManyField(Review)

    def get_genrePref(self):
        return "\n".join([u.name for u in self.genre_pref.all()])

    def get_moviePref(self):
        return "\n".join([u.name for u in self.movie_pref.all()])
    '''
