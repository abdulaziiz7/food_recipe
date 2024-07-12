from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.notification.models import Notification
from apps.recipe.models import RecipeSaved
from apps.user.models import Follow

User = get_user_model()


@receiver(post_save, sender=Follow)
def create_follow(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.following,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk,
            title='New Follower',
            message=f"You have been followed by {instance.following.username}",
        )
