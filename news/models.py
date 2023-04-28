from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse

article = 'A'
news = 'N'

TYPES = [
    (article, 'Статья'),
    (news, 'Новость')
]


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        articles = Post.objects.filter(author=self)
        articles_rating = articles.aggregate(Sum('rating')).get('rating_sum')*3
        comments = Comment.objects.filter(user=self.user)
        comments_rating = comments.aggregate(Sum('rating')).get('rating_sum')
        post_comments = Comment.objects.filter(post_author=self)
        post_comments_rating = post_comments.aggregate(Sum('rating')).get('rating_sum')
        self.rating = articles_rating + comments_rating + post_comments_rating
        self.save()

    def __str__(self):
        return f'{self.user.username} / {self.rating}'


class Category(models.Model):
    cat = models.CharField(max_length=64, default="Default value", unique=True)
    subscribe = models.ManyToManyField(User)


class CategorySubscribe(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subscriber = models.ForeignKey(User, on_delete=models.PROTECT)

class Post(models.Model):
    type = models.CharField(max_length=1, choices=TYPES, default=article)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, through='PostCategory')



    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}'

    def __str__(self):
        return f'{self.type} / {self.title} / {self.date} / {self.rating}'

class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

