from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # ex: /
    url(r'^$', views.review_list, name='review_list'),
    # ex: /review/5/
    url(r'^review/(?P<review_id>[0-9]+)/$', views.review_detail, name='review_detail'),
    # ex: /movie
    url(r'^movie$', views.movie_list, name='movie_list'),
    # ex: /movie/$ search movies for the movie passed in text input
    url(r'^movie/$', views.movie_list, name='movie_list'),
    # ex: /movie/5/
    url(r'^movie/(?P<movie_id>[0-9]+)/$', views.movie_detail, name='movie_detail'),
    # ex: /movie/5/add_review
    url(r'^movie/(?P<movie_id>[0-9]+)/add_review/$', views.add_review, name='add_review'),
    # ex: /review/user/abc - get reviews for the logged user
    url(r'^review/user/(?P<username>\w+)/$', views.user_review_list, name='user_review_list'),
    # ex: /review/user/ - get reviews for the user passed in the url
    url(r'^review/user/$', views.user_review_list, name='user_review_list'),
    # ex: /review/user/5/edit_review - edit reviews for the logged user
    url(r'^review/user/(?P<review_id>[0-9]+)/edit_review/$', views.edit_review, name='edit_review'),
    # ex: /review/user/5/delete_review - delete reviews for the logged user
    url(r'^review/user/(?P<review_id>[0-9]+)/delete_review/$', views.delete_review, name='delete_review'),
    #ex: /review/user/5/delete_review_conf - delete review confirmation
    url(r'^review/user/(?P<review_id>[0-9]+)/delete_review_conf/$',TemplateView.as_view(template_name="reviews\delete_review_conf.html"), name='delete_review_conf'),
    # ex: /recommendation - get movie recommendations for the logged user
    url(r'^recommendation/$', views.user_recommendation_list, name='user_recommendation_list'),
]