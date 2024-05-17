from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.conf import settings
from django.contrib.auth.models import User

class Story(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    picture = models.ImageField(upload_to='media')
    content = CKEditor5Field(config_name='extends', blank=True)
    likes = models.ManyToManyField(User, related_name='post', blank=True)

    def __str__(self):
        return self.topic
