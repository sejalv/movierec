from .models import Movie
ucf = []
def search_movie(request):
    search_movie = (item for item in Movie.objects.all() if item.review_set.count() >=10)
    #print len(movie_list)
    return {'search_movie': search_movie}

def set_uc_flag(request):
    ucf = True

def get_uc_flag(request):
    return {'ucf':ucf}