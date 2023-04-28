from django.forms import ModelForm
from .models import Post, User


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['type', 'title', 'text', 'author', 'categories']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]

