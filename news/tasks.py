from django.core.mail import send_mail
from .models import Category, CategorySubscribe, Post
from datetime import datetime
from .models import User
from django.template.loader import render_to_string
from django.core.mail import send_mail




def send_weekly(instance, action,):

    week_number_last = datetime.now().isocalendar()[1]
    week_posts = Post.objects.filter(created_at__week=str(week_number_last))
    categories1 = Category.objects.all()

    categories_str = []
    for category in categories1:
        categories_str.append(category.cat)

    print(categories_str)

    subscribed_users = []
    for category_subscribe in CategorySubscribe.objects.filter(category__in=instance.categories.all()):
        subscribed_users.append(category_subscribe.subscriber.email)
        posts_of_category = week_posts.filter(post_category_id=category.id)


        for user in subscribed_users:

            print(user)

            message = ''
            for post in posts_of_category:
                message += post.post_text + f'http://127.0.0.1:8000/{post.id}' + '\n'

            send_mail(
                subject=f'Посты за неделю в категории {Category.objects.get(id=category.id)}',
                html_message=render_to_string('weekly_posts.html', context={'link': f'http://127.0.0.1:8000/news/',
                                                                            'user': User.objects.get(
                                                                                id=user.subscriber_id),
                                                                            'category': Category.objects.get(
                                                                                id=category.id),
                                                                            'posts': posts_of_category}),
                message='',
                from_email='egorovarturxx@gmail.com',
                recipient_list=[User.objects.get(id=user.subscriber_id).email]
            )
