from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import PostCategory
from .tasks import send_notification


@receiver(m2m_changed, sender=PostCategory)
def post_withcategory_created(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]
        send_notification.apply_async(
            (instance.preview(), instance.pk, instance.post_title, subscribers), countdown=10,)