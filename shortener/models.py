from django.db import models
from django.contrib.auth.models import User
import random
import string


def generate_short_url():
    # Generate a random short URL
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


class URL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    original_url = models.URLField()
    short_url = models.CharField(max_length=15, unique=True, default=generate_short_url)
    added_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.short_url
