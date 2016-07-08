from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save

class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name='user')

	first_name = models.CharField('First Name', max_length=45, blank=True)
	last_name = models.CharField('Last Name', max_length=45, blank=True)

	phone = models.CharField('Phone', max_length=20, blank=True)
	address = models.CharField('Address', max_length=45, blank=True)
	address2 = models.CharField('Address 2', max_length=45, blank=True)
	city = models.CharField('City', max_length=45, blank=True)
	state = models.CharField('State', max_length=45, blank=True)
	zipcode = models.CharField('Zipcode', max_length=10, blank=True)

	@property
	def email(self):
		return self.user.email

	@property
	def fullname(self):
		return '%S %S' % (self.first_name, self.last_name)

	@property
	def address12(self):
		return ', '.join(addr.strip() for addr in (self.address, self.address2)
						if addr and addr.strip())

	@property
	def full_address(self):
		return '%s, %s, %s, %s' % (self.address12, self.city, self.state, self.zipcode)

def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()
post_save.connect(create_profile, sender=User)
