from .models import Movie
def search_movie(request):
    search_movie = (item for item in Movie.objects.all() if item.review_set.count() >10)
    #print len(movie_list)
    return {'search_movie': search_movie}