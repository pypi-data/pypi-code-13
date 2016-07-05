from django.db import models


class Hotel(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='rooms')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Guest(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='guests')
    room = models.ForeignKey(Room, related_name='guests', null=True, blank=True)
    name = models.CharField(max_length=200)
