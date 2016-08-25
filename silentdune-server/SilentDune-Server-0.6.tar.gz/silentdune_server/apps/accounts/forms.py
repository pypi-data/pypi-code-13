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

__author__ = 'Robert Abram'

from django import forms
from django.contrib.auth.hashers import check_password
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404


# TODO: Review all validation error messages for all fields

class SDAuthenticationForm(forms.Form):

    # Override the form user and password objects to work with Bootstrap
    username = forms.CharField(
        label=_('Username'),
        max_length=254,
        widget=forms.TextInput(attrs={
            'placeholder': _('Username'),
            'class': 'form-control',
            'required': 'true'
        })
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Password'),
            'class': 'form-control',
            'required': 'true'
        })
    )



class Profile(forms.Form):

    error_messages = {
        'duplicate_username': _("A user with that user name already exists."),
        'duplicate_email': _("A user with that email already exists."),
        'password_mismatch': _("The two password fields didn't match."),
        'email_mismatch': _("The two email fields didn't match."),
        'invalid_current_password': _("Your current password is incorrect."),
    }

    email = forms.EmailField(
        label=_('New email address'),
        required=False,
        error_messages={'required': _('Enter a valid email address.')},
        widget=forms.EmailInput(attrs={'placeholder': _('Email address'), 'class': 'email'}),
    )

    email_password = forms.CharField(
        label=_('Current password'),
        required=False,
        validators=[MinLengthValidator(8)],
        widget=forms.PasswordInput(attrs={'placeholder': _('Password'), 'class': 'password'}),
    )

    username = forms.CharField(
        label=_('New user name'),
        required=False,
        validators=[MinLengthValidator(3)],
        widget=forms.TextInput(attrs={'placeholder': _('User name')}),

    )

    username_password = forms.CharField(
        label=_('Current password'),
        required=False,
        validators=[MinLengthValidator(8)],
        widget=forms.PasswordInput(attrs={'placeholder': _('Password'), 'class': 'password'}),
    )

    old_password = forms.CharField(
        label=_('Current password'),
        required=False,
        validators=[MinLengthValidator(8)],
        widget=forms.PasswordInput(attrs={'placeholder': _('Password'), 'class': 'password'}),
    )

    new_password = forms.CharField(
        label=_('New password'),
        required=False,
        validators=[MinLengthValidator(8)],
        widget=forms.PasswordInput(attrs={'placeholder': _('Password'), 'class': 'password'}),
    )

    new_password2 = forms.CharField(
        label=_('Retype new password'),
        required=False,
        validators=[MinLengthValidator(8)],
        widget=forms.PasswordInput(attrs={'placeholder': _('Password'), 'class': 'password'}),
    )

    action = forms.CharField(
        widget=forms.HiddenInput,
        required=False,
    )

    class Meta:
        fields = ('email', 'email_password', 'username', 'username_password', 'old_password',
                  'new_password', 'new_password2', 'action')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(Profile, self).__init__(*args, **kwargs)

    def clean_email_password(self):

        pwd = self.cleaned_data.get('email_password')

        if pwd and check_password(pwd, self.user.password) == False:
            raise forms.ValidationError(
                self.error_messages['invalid_current_password'],
                code='invalid_current_password',
            )

        return pwd

    def clean_username_password(self):

        pwd = self.cleaned_data.get('email_password')

        if pwd and check_password(pwd, self.user.password) == False:
            raise forms.ValidationError(
                self.error_messages['invalid_current_password'],
                code='invalid_current_password',
            )

        return pwd

    def clean_old_password(self):

        pwd = self.cleaned_data.get('old_password')

        if pwd and check_password(pwd, self.user.password) == False:
            raise forms.ValidationError(
                self.error_messages['invalid_current_password'],
                code='invalid_current_password',
            )

        return pwd

    def clean_new_password2(self):

        new_pwd = self.cleaned_data.get('new_password')
        new_pwd2 = self.cleaned_data.get('new_password2')

        if new_pwd and new_pwd2 and new_pwd != new_pwd2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

        return new_pwd2

    def save_email(self, commit=True):

        self.user.email = self.cleaned_data.get('email')

        if commit:
            self.user.save();

        return self.user

    def save_username(self, commit=True):

        self.user.user_name = self.cleaned_data.get('username')

        if commit:
            self.user.save();

        return self.user

    def save_password(self, commit=True):

        self.user.set_password(self.cleaned_data.get('new_password2'))

        if commit:
            self.user.save()

        return self.user



