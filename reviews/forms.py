from django.forms import ModelForm, Textarea, TextInput
from reviews.models import Review, Movie


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        #fields = ['rating', 'comment']
        fields = ['comment']
        widgets = {
         #   'rating': TextInput(attrs={'class':"star"}),
            'comment': Textarea(attrs={'cols': 10, 'rows': 2}),
        }
'''
class ReviewMovieForm(ModelForm):
    class Meta:
        model = Review
        fields = ['movie','rating', 'comment']
        widgets = {
            'comment': Textarea(attrs={'cols': 10, 'rows': 5}),
        }
'''
