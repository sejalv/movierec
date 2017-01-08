import sys, os 
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movierec.settings")

import django, re
django.setup()

from reviews.models import Movie, Genre


def save_movie_from_row(movie_row):
    movie = Movie()
    '''
    try:
        movie.id = Movie.objects.last().pk + 1  #movie_row[0]
    except: #TypeError:
        movie.id = 1
    '''
    movie.id = movie_row[0]
    movie.name = movie_row[1].strip()
    #movie.year = movie.name[-5:-1]
    try:
        movie.duration = movie.name[movie.name.rfind("(") + 1:movie.name.rfind(")")].strip()
    except movie.name.rfind("(") == -1 and movie.name.rfind(")") == -1:
        movie.duration = None
    movie.save()
    #movie.duration = .strip("!@#$%^&*()[]{};:,./<>?\|`~-=_+")

    movie_genres = [x.strip() for x in movie_row[2].split("|")]
    movie.genres.add(*Genre.objects.filter(name__in=movie_genres))  # [i]))
    '''
    for g in movie_genres:
        movie.genres.add(Genre.objects.get(name=g)) #[i]))
    '''
    movie.save()
    
    
if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        print "Reading from file " + str(sys.argv[1])
        movies_df = pd.read_csv(sys.argv[1])
        print movies_df

        movies_df.apply(
            save_movie_from_row,
            axis=1
        )

        print "There are {} movies".format(Movie.objects.count())
        
    else:
        print "Please, provide Movie file path"
