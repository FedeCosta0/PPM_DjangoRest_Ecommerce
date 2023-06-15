from PPM_Ecommerce_API import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def report_uploaded(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
