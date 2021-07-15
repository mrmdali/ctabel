from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account, Worker


def create_related_profile(sender, instance, created, *args, **kwargs):
    if created:
        Worker.objects.create(account=instance)


post_save.connect(create_related_profile, sender=Account)
