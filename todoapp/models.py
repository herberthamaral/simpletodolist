from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    name = models.CharField(max_length='140')
    done = models.BooleanField(default=False)
    time_in_seconds = models.IntegerField(default=0)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.name
