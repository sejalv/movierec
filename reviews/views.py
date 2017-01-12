from django.shortcuts import get_object_or_404, render, HttpResponse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Review, Movie, Cluster
from .forms import ReviewForm
from .suggestions import update_clusters
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from django.db.models

import datetime
# import requests, json, sys    # new


def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'reviews/review_list.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    form = ReviewForm()
    return render(request, 'reviews/review_detail.html', {'review': review, 'form': form})


def movie_list(request):
    if request.GET.get('search'):
        #movie_id = request.GET['search']
        movie_list = Movie.objects.filter(name__icontains=request.GET['search'])
    else:
        movie_list = Movie.objects.order_by('name')

    paginator = Paginator(movie_list, 100)  # Show 100 movies per page
    page = request.GET.get('page')
    try:
        movie_list = paginator.page(page)
    except PageNotAnInteger: # If page is not an integer, deliver first page.
        movie_list = paginator.page(1)
    except EmptyPage: # If page is out of range (e.g. 9999), deliver last page of results.
        movie_list = paginator.page(paginator.num_pages)

    '''
       movie_list = sorted(
       Movie.objects.all(),
       #key=lambda x: x.average_rating,
       key=lambda x: x.review_set.count(),
       reverse=True
    )
    '''
    context = {'movie_list':movie_list}
    return render(request, 'reviews/movie_list.html', context)

'''
    # api - json res
    req = requests.get('http://www.omdbapi.com/?i=tt1285016')
    content = req.text
    return HttpResponse(content)
'''

def movie_detail(request, movie_id): #, error_message=None):
    movie = get_object_or_404(Movie, pk=movie_id)
    try:
        user = User.objects.get(username=request.user.username)
        review = Review.objects.get(user_name=user, movie=movie)
        #review=get_object_or_404(r,pk=r.id)
        return render(request, 'reviews/movie_detail.html', {'review':review, 'movie': movie})
    except:
        form = ReviewForm()
        return render(request, 'reviews/movie_detail.html', {'movie': movie, 'form': form})  # , 'error_message':error_message})


@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    form = ReviewForm(request.POST)
    if form.is_valid() and request.POST: #.get('sbmt'):
        try:
            #rating = form.cleaned_data['rating']
            comment = form.cleaned_data['comment']
            rating = request.POST['sbmtBtn']  # ",False)
            user_name = request.user.username
            review = Review()
            review.movie = movie
            review.user_name = User.objects.get(username=user_name)
            # review.user = User.objects.get(username=user_name)
            review.rating = rating
            review.comment = comment
            #review.pub_date = datetime.datetime.now()
            review.pub_date = timezone.now()
            review.save()
            #update_clusters()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('reviews:movie_detail', args=(movie.id,)))
        except:
            return HttpResponseRedirect(reverse('reviews:movie_detail', args=(movie.id))) #,"Please enter a rating!")))
    return render(request, 'reviews/movie_detail.html', {'movie': movie, 'form': form}) #, 'error_message':error_message})
    

def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
    # latest_review_list = Review.objects.filter(user=User.objects.get(username=user_name).pk).order_by('-pub_date')
    # form = ReviewMovieForm()
    context = {'latest_review_list':latest_review_list, 'username':username} #, 'form':form}
    return render(request, 'reviews/user_review_list.html', context)


@login_required
def edit_review(request, review_id): #=None):
    #if review_id:
    review = get_object_or_404(Review, pk=review_id)
    username = User.objects.get(username=request.user.username)
    if review.user_name != username:
        return HttpResponseForbidden()
    #else: review = Review(user_name=request.user.username)
    form = ReviewForm(request.POST or None, instance=review)
    if request.POST and form.is_valid():
        try:
            review.rating = request.POST.get('sbmtBtn')
            review.pub_date = datetime.datetime.now()
            form.save()
            #update_clusters()
            # Save was successful, so redirect to another page # redirect_url = reverse('reviews:movie_detail', args=(movie.id,)))
            return HttpResponseRedirect(reverse('reviews:review_detail', args=(review.id,)))
        except:
            #raise validationerror
            return HttpResponseRedirect(reverse('reviews:review_detail', args=(review.id,)))
    return render(request, 'reviews/review_detail.html', {'review':review, 'form': form})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    username=User.objects.get(username=request.user.username)
    if review.user_name != username:
        return HttpResponseForbidden()
    #form = ReviewForm(request.POST or None, instance=review)

    if request.POST: #.get("Delete"): #POST.get for button values not working
        # when confirmation page has been displayed and confirm button pressed
        review.delete()
        #update_clusters()
        return HttpResponseRedirect(reverse('reviews:user_review_list'))
    '''
    elif request.POST.get("No"):    #POST.get for button values not working
        # when confirmation page has been displayed and cancel button pressed
        return HttpResponseRedirect(reverse('reviews:user_review_list'))
    '''
    return render(request, 'reviews/user_review_list.html') #, {'username':username}) #, {'review':review, 'form': form})

@login_required
def user_recommendation_list(request):
    # get request user reviewed movies
    user=User.objects.get(username=request.user.username)
    user_reviews = Review.objects.filter(user_name=user).prefetch_related('movie')
    user_reviews_movie_ids = set(map(lambda x: x.movie.id, user_reviews))

    # get request user cluster name (just the first one right now)
    try:
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name
    except: # if no cluster assigned for a user, update clusters
        update_clusters()
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name

    # get usernames for other members of the cluster
    user_cluster_other_members = \
        Cluster.objects.get(name=user_cluster_name).users \
            .exclude(username=request.user.username).all()

    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

    # get reviews by those users, excluding movies reviewed by the request user
    other_users_reviews = \
        Review.objects.filter(user_name__in=other_members_usernames) \
            .exclude(movie__id__in=user_reviews_movie_ids)

    other_users_reviews_movie_ids = set(map(lambda x: x.movie.id, other_users_reviews))

    '''
    # then get a movie list including the previous IDs, order by rating
    movie_list = sorted(
        list(Movie.objects.filter(id__in=other_users_reviews_movie_ids)),
        #Movie.objects.filter(id__in=other_users_reviews_movie_ids),
        key=lambda x: x.average_rating,
        reverse=True
    )
    '''
    #print len(other_users_reviews_movie_ids)
    vals_all = Movie.objects.all()
    vals_filtered = (item for item in vals_all if item.id in other_users_reviews_movie_ids and item.review_set.count() >= 10)
    movie_list = sorted(vals_filtered, key=lambda x: x.review_set.count(), reverse=True)[:10]
    #movie_list = [(v.id, v.name) for v in vals_ordered][:20]

    #movie_list = Movie.objects.filter(id__in=other_users_reviews_movie_ids)
    #print len(movie_list)

    return render(
        request, 
        'reviews/user_recommendation_list.html', 
        {'username': request.user.username,
         'movie_list': movie_list}
    )

