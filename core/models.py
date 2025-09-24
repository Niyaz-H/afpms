from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """
    Extends the default User model to include user roles.
    """
    class Role(models.TextChoices):
        FACTORY_MANAGER = 'FACTORY_MANAGER', 'Factory Manager'
        DEMAND_PLANNER = 'DEMAND_PLANNER', 'Demand Planner'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.DEMAND_PLANNER
    )

    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal receiver to create or update the user profile automatically.
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
