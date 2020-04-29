from django.db import models
from django.contrib.auth.models import User

# Developer friendly variables for the different status of an event
STATUS_OPEN = 0
STATUS_DECIDED = 1


class Status(models.Model):
    """Table that holds two values for defining the status of an event
    If an event is open, proposals can be given
    If the event is in status "DECIDED", the organisator determined the final date,time,place and no proposals can
    be given anymore
    """
    STATUS = (
        (STATUS_OPEN, 'OPEN'),
        (STATUS_DECIDED, 'DECIDED')
    )
    status = models.IntegerField(choices=STATUS)


class Event(models.Model):
    """Table that stores data about the events
    """
    title = models.CharField(max_length=100)  # title/short description of the event
    organisator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organisator')  # user that created
                                                                                                 # the event
    status = models.ForeignKey(Status, on_delete=models.CASCADE)  # status can be OPEN or DECIDED
    date = models.DateField()  # date of the event
    time = models.TimeField()  # time of the event
    duration = models.IntegerField() # duration in minutes
    place = models.CharField(max_length=100)  # place of the event
    guests = models.ManyToManyField(User, related_name='guests')   # many to many field for all the users that are
                                                                   # invited
    comment = models.CharField(max_length=200)  # comment that is given from the organisator when he determines
                                                # the final event

    def get_event_status_str(self):
        if self.status.status == STATUS_OPEN:
            return 'Offen für Vorschläge'
        else:
            return 'Termin festgelegt'

    def event_is_open(self):
        if self.status.status == STATUS_OPEN:
            return True
        else:
            return False

    def get_date_str(self):
        return str(self.date.day) + '.' + str(self.date.month) + '.' + str(self.date.year)

    def get_time_str(self):
        return str(self.time)


class Proposal(models.Model):
    """Table that contains the proposals given from users"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # the key of the event to which this proposal belongs
    date = models.DateField()  # proposed date
    time = models.TimeField()  # proposed time
    place = models.CharField(max_length=100)  # proposed place
    comment = models.CharField(max_length=200)  # custom comment from the user
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_user')  # the key of the user
                                                                                            # that wrote the proposal
