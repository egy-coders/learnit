from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from .models import User, StudentProfile, InstructorProfile

User = get_user_model()

@receiver(post_save, sender=User)
def invalidate_tokens_on_role_change(sender, instance, **kwargs):
    if instance.pk:  # Check if the instance is being updated
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.role != instance.role:  # Role has changed
            tokens = OutstandingToken.objects.filter(user=instance)
            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)


# Auto create profile student on new user
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'student':
            StudentProfile.objects.get_or_create(user=instance)
        elif instance.role == 'instructor':
            InstructorProfile.objects.get_or_create(user=instance)


# change role from student to instructor / admin will delete student profile
@receiver(pre_save, sender=User)
def update_user_profile(sender, instance, **kwargs):
    if not instance.pk:
        return  # New user handled in post_save

    old_user = User.objects.get(pk=instance.pk)
    old_role = old_user.role
    new_role = instance.role

    if old_role != new_role:
        # Delete old profile
        if old_role == 'student':
            StudentProfile.objects.filter(user=instance).delete()
        elif old_role == 'instructor':
            InstructorProfile.objects.filter(user=instance).delete()

        # Create new profile
        if new_role == 'student':
            StudentProfile.objects.get_or_create(user=instance)
        elif new_role == 'instructor':
            InstructorProfile.objects.get_or_create(user=instance)
