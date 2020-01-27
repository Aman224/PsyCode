from django.db import models
from django.urls import reverse

class Content(models.Model):
    inputData = models.TextField()
    outputData = models.TextField()

    def get_absolute_url(self):
        return reverse('home')