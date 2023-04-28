from django_filters import FilterSet
from django import forms
from .models import Post, Author


class NewsFilter(FilterSet):
   class Meta:
       model = Post
       fields = {
           'title': ['icontains'],
           'author': ['exact'],
           'date': ['gt'],
       }

