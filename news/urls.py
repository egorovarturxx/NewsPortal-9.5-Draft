from django.urls import path
from .views import (NewsList, NewsDetail, NewsSearch, CreatePost, EditPost, DeletePost, upgrade_me, CategoriesView, CategoryDetail, subscribe_to_category)


urlpatterns = [
   path('', NewsList.as_view(), name='home'),
   path('<int:pk>', NewsDetail.as_view(), name='post_detail'),
   path('search/', NewsSearch.as_view(), name='search'),
   path('create', CreatePost.as_view(), name='news_create'),
   path('<int:pk>/edit', EditPost.as_view(), name='news_update'),
   path('<int:pk>/delete', DeletePost.as_view(), name='news_delete'),
   path('create/upgrade/', upgrade_me, name='upgrade'),
   path("categories/", CategoriesView.as_view()),
   path('categories/<int:pk>', CategoryDetail.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe_to_category, name='subscribe'),
]