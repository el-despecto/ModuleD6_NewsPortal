from django_filters import FilterSet
from .models import Post



class PostFilter(FilterSet):

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author': ['in'],
            'dateCreation': ['date'],
            'rating_post': ['lt'],
        }