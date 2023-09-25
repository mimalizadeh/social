from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('acc')

    def __str__(self):
        return f"{self.from_user} following {self.to_user}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    age = models.PositiveSmallIntegerField(default=0)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(max_length=400, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} is {self.age} old"
