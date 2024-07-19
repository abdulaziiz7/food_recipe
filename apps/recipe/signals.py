from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.notification.models import Notification
from apps.recipe.models import RecipeSaved, Comment, CommentLike, Recipe

User = get_user_model()


@receiver(post_save, sender=RecipeSaved)
def save_recipe(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.recipe.user,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk,
            title='Save Recipe Alert',
            message=f"Your recipe '{instance.recipe.title}' has been saved by {instance.user.username}"
        )


@receiver(post_save, sender=Comment)
def comment_recipe(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.recipe.user,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk,
            title='New Comment!',
            message=f"Comment: {instance.text}\nOn Recipe: {instance.recipe.title}\nBy {instance.user.username} "
        )


@receiver(post_save, sender=CommentLike)
def comment_liked(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.comment.user,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk,
            title='Your Comment Was Liked!',
            message=f"Your comment '{instance.comment.text}' has been liked by {instance.user.username}"
        )


@receiver(post_save, sender=Recipe)
def new_recipe(sender, instance, created, **kwargs):
    # if created:
    for follow in instance.user.following.all():
        Notification.objects.create(
            user=follow.follower,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk,
            title='New Recipe!',
            message=f"New recipe was created by {instance.user.username}"
        )
