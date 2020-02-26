from django.db import models
from django.urls import reverse


LANGUAGES = (
    ('c','C'),
    ('python','Python'),
)


class Content(models.Model):
    inputData = models.TextField()
    language = models.CharField(max_length=10, choices=LANGUAGES, default='python')
    outputData = models.TextField()

    def get_absolute_url(self):
        return reverse('home')