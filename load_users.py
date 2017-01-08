import sys, os 
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movierec.settings")

import django
django.setup()

from django.contrib.auth.models import User


def save_user_from_row(user_row):
   user = User()
   try:
       user.id = User.objects.last().pk + 1  #user_row[0]
   except: #TypeError:
       user.id = 1
   user.username = user_row[1]
   user.save()
    
    
if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        print "Reading from file " + str(sys.argv[1])
        users_df = pd.read_csv(sys.argv[1])
        print users_df
        users_df.apply(
            save_user_from_row,
            axis=1
        )

        print "There are {} users".format(User.objects.count())
        
    else:
        print "Please, provide User file path"
