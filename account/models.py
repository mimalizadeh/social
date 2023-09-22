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
