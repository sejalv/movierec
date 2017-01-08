import sys, os 
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movierec.settings")

import django
django.setup()

from reviews.models import Genre


def save_genre_from_row(genre_row):
    genre = Genre()
    genre.id = genre_row[0]
    genre.name = genre_row[1].strip()
    genre.save()
    
    
if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        print "Reading from file " + str(sys.argv[1])
        genres_df = pd.read_csv(sys.argv[1])
        print genres_df

        genres_df.apply(
            save_genre_from_row,
            axis=1
        )

        print "There are {} genres".format(Genre.objects.count())
        
    else:
        print "Please, provide Genre file path"
