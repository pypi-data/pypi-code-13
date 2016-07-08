from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

SHELTER = 'shelter'
FOOD = 'food'
SOCIAL = 'social'
CLOSED = 'closed'
OPEN = 'open'
RESERVE = 'reserve'


class Organization(models.Model):

    ORGANIZATION_TYPE_CHOICES = (
        (SHELTER, SHELTER.capitalize()),
        (FOOD, FOOD.capitalize()),
        (SOCIAL, SOCIAL.capitalize()),
    )

    ORGANIZATION_OPEN_CHOICES = (
        (CLOSED, CLOSED.capitalize()),
        (OPEN, OPEN.capitalize()),
        (RESERVE, RESERVE.capitalize()),
    )
    creator = models.ForeignKey('auth.User', related_name='creator', on_delete=models.CASCADE)

    name = models.CharField(max_length=50, blank=True)
    description = models.TextField('Description', max_length=1000, blank=True)
    email = models.EmailField('Email', max_length=50, blank=True)
    address = models.CharField('Address', max_length=30, blank=True)
    phone = models.CharField('Phone', max_length=250, blank=True)
    max_volunteers = models.IntegerField('Max Volunteers', null=True, blank=True)
    min_volunteers = models.IntegerField('Minimum Volunteers', null=True, blank=True)


    def __str__(self):              # __unicode__ on Python 2
        return self.name

    def get_absolute_url(self):
        return reverse('organization_detail_view', kwargs={'pk': self.pk})

    '''
    @classmethod
    def create_org(
        cls, creator, name, description,email,
        address, phone, max_volunteers, min_volunteers
    ):
        obj = cls.objects.create(
            creator=creator,
            name=name,
            description=description,
            email=email,
            address=address,
            phone=phone,
            max_volunteers=max_volunteers,
            min_volunteers=min_volunteers,
        )

    @classmethod
    def update_org(
        cls, organization, creator, name, description,
        address, phone, max_volunteers, min_volunteers
    ):
        obj = cls.objects.get(pk=organization)
        obj.name = name
        obj.description = description
        obj.address = address
        obj.phone = phone
        obj.max_volunteers = max_volunteers
        obj.min_volunteers = min_volunteers
        obj.save()
        '''
