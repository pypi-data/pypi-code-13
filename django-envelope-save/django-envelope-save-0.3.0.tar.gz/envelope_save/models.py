# -*- coding: utf-8 -*-

from django.db import models
from django.dispatch import receiver
from envelope.forms import ContactForm
from envelope.signals import before_send
from model_utils.models import TimeStampedModel


class Contact(TimeStampedModel):
    sender = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(blank=True)

    def __str__(self):
        return '{} ({})'.format(self.sender, self.email)


@receiver(before_send)
def save_contact(sender, **kwargs):
    if isinstance(kwargs['form'], ContactForm):
        Contact.objects.create(sender=kwargs['form'].data['sender'],
                               email=kwargs['form'].data['email'],
                               message=kwargs['form'].data['message'])
    return True
