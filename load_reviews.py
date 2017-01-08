import sys, os 
import pandas as pd
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movierec.settings")

import django
django.setup()

from django.contrib.auth.models import User
from reviews.models import Review, Movie


def save_review_from_row(review_row):
    review = Review()
    try:
        review.id = Review.objects.last().pk + 1     #review_row[0]
    except: #TypeError:
        review.id = 1
   # print review_row[1]
   # print str(review_row[1])
   # print str(int(review_row[1]))
   # print "%10.0f" % review_row[1]
    user = User.objects.get(username=''+str(int(review_row[1])))
    review.user_name = user
    #review.user_name = User.objects.get(id=review_row[1])
    review.movie = Movie.objects.get(id=review_row[2])
    review.rating = review_row[3]
    review.comment = review_row[4]
    review.pub_date = datetime.datetime.now()
    # review.pub_date = review_row[5].strip() if review_row[5].strip() else datetime.datetime.now()
    review.save()
    
    
if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        print "Reading from file " + str(sys.argv[1])
        reviews_df = pd.read_csv(sys.argv[1])
        print reviews_df
        reviews_df.apply(
            save_review_from_row,
            axis=1
        )

        print "There are {} reviews in DB".format(Review.objects.count())
        
    else:
        print "Please, provide Reviews file path"
