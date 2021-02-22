from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class BugHunter(AbstractUser):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    REQUIRED_FIELDS = ["first_name", "last_name"]


# Generates unique email for users on creation.
@receiver(pre_save, sender=BugHunter)
def generate_email(sender, instance, *args, **kwargs):
    if not instance.email:
        email_prefix = f"{instance.first_name[:1]}{instance.last_name}".lower()
        email_suffix = "@bigbadbughunter.com"
        if BugHunter.objects.filter(email=f"{email_prefix}{email_suffix}".lower()):
            id_num = 1
            while BugHunter.objects.filter(
                email=f"{email_prefix}{email_suffix}".lower()
            ):
                email_prefix = (
                    f"{instance.first_name[:1]}{instance.last_name}".lower()
                    + str(id_num)
                )
                id_num += 1
        instance.email = f"{email_prefix}{email_suffix}".lower()


class Ticket(models.Model):
    title = models.CharField(max_length=64)
    time = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    filed_by = models.ForeignKey(
        BugHunter, related_name="filer", on_delete=models.CASCADE
    )
    assigned_to = models.ForeignKey(
        BugHunter, related_name="assignee", on_delete=models.CASCADE
    )
    completed_by = models.ForeignKey(
        BugHunter, related_name="hero", on_delete=models.CASCADE
    )

    STATUS_CHOICES = [
        ("NEW", "New"),
        ("IN_PROGRESS", "In Progress"),
        ("DONE", "Done"),
        ("INVALID", "Invalid"),
    ]
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="NEW")
