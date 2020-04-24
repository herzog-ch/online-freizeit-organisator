from django.db import models
from django.contrib.auth.models import User

STATUS_OPEN = 0
STATUS_DECIDED = 1


class Status(models.Model):
    STATUS = (
        (STATUS_OPEN, 'OPEN'),
        (STATUS_DECIDED, 'DECIDED')
    )
    status = models.IntegerField(choices=STATUS)


class Event(models.Model):
    title = models.CharField(max_length=100)
    organisator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organisator')
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    # proposals = models.ManyToManyField(Proposal)
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField() # duration in minutes
    place = models.CharField(max_length=100)
    guests = models.ManyToManyField(User, related_name='guests')


class Proposal(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    place = models.CharField(max_length=100)
    comment = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_user')
    upvotes = models.ManyToManyField(User)
