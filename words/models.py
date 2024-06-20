from django.db import models
from django.utils import timezone
from accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Word(models.Model):
    name = models.CharField(max_length=250)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    english = models.CharField(max_length=250, default='')
    uzb = models.CharField(max_length=250, default='')
    example_en = models.TextField(max_length=500, default='')
    example_uz = models.TextField(max_length=500, default='')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

