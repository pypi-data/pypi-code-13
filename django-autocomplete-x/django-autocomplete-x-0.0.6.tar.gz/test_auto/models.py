from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django_autocomplete import models as fields

class MyModel2(User):
	name = models.CharField(max_length=45)

	def __unicode__(self):
		return self.name
	# end def
# end class


class MyModel(models.Model):
	name = models.CharField(max_length=45)
	ref = fields.AutocompleteRelation(MyModel2)
# end class

