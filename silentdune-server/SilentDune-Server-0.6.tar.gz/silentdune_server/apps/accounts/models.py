#
# Authors: Robert Abram <robert.abram@entpack.com>
#
# Copyright (C) 2015 EntPack
# see file 'LICENSE' for use and warranty information
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django_countries.fields import CountryField
import datetime

# Add the user profile to the django.contrib.auth.models.User object and
# auto create the user profile database record if it does not exist
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

# UserProfile gets attached the User database object. IE: User.profile.url
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('read write', _('Read/Write')),
        ('read', _('Read Only')),
    )

    user = models.OneToOneField(User)
    accepted_terms = models.BooleanField(default=False)
    email_reg_code = models.CharField(max_length=25, db_index=True)
    account_activated = models.BooleanField(default=False)
    oauth_scope = models.CharField(max_length=255, choices=ROLE_CHOICES, default='read write') #'read write')
    utc_offset = models.CharField(max_length=10, default='+00:00')

    class Meta:
        db_table = 'auth_user_profile'
        
class UserProfileEditForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['oauth_scope', 'utc_offset']
        
class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']      
        
#class MyUserChangeForm(UserChangeForm):
    #def __init__(self, *args, **kwargs):
        #super(MyUserChangeForm, self).__init__(*args, **kwargs)
        #del self.fields['password']

    #class Meta:
        #model = User
        #fields = ('username','email','first_name','last_name')        
        
        






