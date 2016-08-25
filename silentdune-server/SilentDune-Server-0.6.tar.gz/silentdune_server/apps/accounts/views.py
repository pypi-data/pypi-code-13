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

import json 

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import activate, FixedOffset, get_fixed_timezone

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django import forms 
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from apps.accounts.models import UserProfile
from apps.accounts.models import UserProfileEditForm, UserEditForm
from apps import accounts
from apps.alerts.models import *
from proj.common.oauth_helper import create_access_token, encrypt_access_token

utc_offsets = ['-14:00','-13:00','-12:00','-11:00','-10:00','-09.30','-09:00','-08:00','-07:00','-06:00',
               '-05:00','-04:00','-03:00','-02:00','-01:00','+00:00','+01:00','+02:00','+03:00','+03:30',
               '+04:00','+04:30','+05:00','+05.30','+05:45','+06:00','+07:00','+08:00','+08:30','+08:45',
               '+09:00','+09:30','+10:00','+10:30','+11:00','+12:00','+12:45'] 

@csrf_exempt
def sdLogin(request, *args, **kwargs):

    # TODO: Support the "next" parameter in the template javascript redirect code.

    # This POST method is called by javascript and expects some JSON in return.
    # The goal here is to authenticate the user with oauth and then encrypt the
    # oauth information.  The encrypted information will be stored in a browser cookie,
    # to be later decrypted in the middleware level to set the "Authorization" header.
    if request.method == 'POST':

        if 'username' not in request.POST or 'password' not in request.POST:
            raise ValueError

        # Manually do django authentication.
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:

            # Log our user in to django
            login(request, user)

            # Create and encrypt the access token based on this user
            enc = encrypt_access_token(create_access_token(user, user.profile.oauth_scope))

            # Setup login redirect
            if 'next' in request.GET:
                redirect = request.GET['next']
            else:
                redirect = settings.LOGIN_REDIRECT_URL

            # Format our response
            response = JsonResponse(
                dict([('status', 'OK'), ('next', redirect)])
            )

            # Set the encrypted token in the response.
            response.set_cookie('token', enc.decode('UTF-8'))
            response.set_cookie('fade-page-in', 1)

        else:
            # Send our error message
            response = JsonResponse(
                dict([('status', 'ERROR')])
            )

        return response

    else:

        form = accounts.forms.SDAuthenticationForm()
        context = {
            'form': form,
            'next': request.GET['next'] if 'next' in request.GET else None,
        }

    return render(request, 'accounts/login.html', context)


@login_required
def profiles(request):
    context = {}
    context['alert_count'] = Alerts.objects.filter(soft_delete=False).count()
    # Display a list of user profiles for CRUDing 
    users_per_page = 20
    cleaner = forms.CharField()
    
    #set user timezone
    user_offset = UserProfile.objects.get(user = request.user).utc_offset
    user_offset_in_minutes = int(user_offset[1:3]) * 60 + int(user_offset[4:6])
    if user_offset[0] == '-': user_offset_in_minutes *= -1
    
    this_tzinfo = get_fixed_timezone(user_offset_in_minutes)
    activate(this_tzinfo)
    
    
    context["allow_edit"] = True
    
    # If user is not permitted to make changes reset the allow_edits flag
    if UserProfile.objects.get(user = request.user).oauth_scope == "read" :
        context["allow_edit"] = False    
    
    if request.method == "POST" and request.POST.get('search_term'):
        #Display a list of users that match the search term
        search_term = cleaner.clean(request.POST['search_term'])
        
        all_users = UserProfile.objects.filter(Q(user__username__icontains=search_term) | Q(user__first_name__icontains=search_term)
                                             | Q(user__last_name__icontains=search_term)).filter(user__is_active=True).distinct()
                                             
       #set up this page of users and pagination values
        paginator = Paginator(all_users, users_per_page)
        page = request.GET.get('page')
        
        try:
            these_users = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            these_users = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)                                             
        context['use_pagination'] = False                                  
        context['page_of_users'] = these_users
        context['the_term'] = search_term
        
    else:
        if request.GET.get('term', '') == '':
            # no incoming search term so get all users
            all_users = UserProfile.objects.all()
        else:
            # use the search term to create a query set of matching users
            search_term = cleaner.clean(request.GET.get('term',''))
            context['the_term'] = search_term
            all_users = UserProfile.objects.filter(Q(user__username__icontains=search_term) | Q(user__first_name__icontains=search_term)
                                             | Q(user__last_name__icontains=search_term)).filter(user__is_active=True).distinct()   
        
        #set up this page of users and pagination values
        paginator = Paginator(all_users, users_per_page)
        
        page = request.GET.get('page')
        
        try:
            these_users = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            these_users = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)        
        
        context['use_pagination'] = True
        context['page_of_users'] = these_users
        context["allow_edit"] = True
    
    return render(request, 'accounts/profile.html', context)
    
    
@login_required
def edit(request, upk): 
    context = {}
    context['alert_count'] = Alerts.objects.filter(soft_delete=False).count()
    
    cleaner = forms.CharField()
    context['utc_offsets'] = utc_offsets
    
    #get the user of the site
    this_profile = UserProfile.objects.get(user = request.user)
    this_user = User.objects.get(id=request.user.id)    
    
    
    # the user that's being edited    
    upk = int(cleaner.clean(upk))
    edit_user_profile = UserProfile.objects.get(user=upk)
    edit_user = User.objects.get(id=edit_user_profile.user.id) 
    
    context['user_data'] = edit_user_profile
    
    if 'write' in this_profile.oauth_scope.split():
        context['can_edit'] = True
        if request.method == "POST":
                
            user_profile_edit_form = UserProfileEditForm(request.POST)
            user_edit_form = UserEditForm(request.POST, instance=request.user)
            if user_edit_form.is_valid() and user_profile_edit_form.is_valid():
                #set default edit message
                context['edit_msg'] = "User data successfully saved."
                
                #Clean independent form values
                user_id = cleaner.clean(request.POST['user_id'])
                username = cleaner.clean(request.POST['username'])
                
                valid_ids = True
                
                if edit_user.id != upk:
                    #if user's id's don't match then return to form.
                    context['edit_msg'] = "User data could not be saved."
                    valid_ids = False
                    
                if not valid_ids:
                    #if errors exist return to page and display error message    
                    return render(request, 'accounts/edit_profile.html', context)
                    
                # save the 'user' data that has been edited
                edit_user.username = username
                edit_user.first_name = user_edit_form.cleaned_data['first_name']
                edit_user.last_name = user_edit_form.cleaned_data['last_name']
                edit_user.email = user_edit_form.cleaned_data['email']
                edit_user.save() 
                
                # Save the 'profile' data
                edit_user_profile.oauth_scope = user_profile_edit_form.cleaned_data['oauth_scope']
                edit_user_profile.utc_offset = user_profile_edit_form.cleaned_data['utc_offset']
                edit_user_profile.save()                               
                
                # reload from the database to update all data going to the template
                edit_user_profile = UserProfile.objects.get(user=upk)
                
                context['user_data'] = edit_user_profile
                
            else:
              context['edit_msg'] = "Input data is not valid."    

    
    # If any of the following fields is empty then set it to value of its generic label 
    # for populating the placeholder values in the form.
    if not edit_user_profile.user.first_name :
        edit_user_profile.user.first_name = 'First name'
    if not edit_user_profile.user.last_name :
        edit_user_profile.user.last_name = 'Last name' 
    if not edit_user_profile.user.email :
        user_data.user.email = 'Email address'
    return render(request, 'accounts/edit_profile.html', context)
    


@login_required
def delete(request, upk): 
    context = {}
    
    #check if user is allowed to delete
    this_profile = UserProfile.objects.get(user = request.user)
    if this_profile.oauth_scope == 'read':
        return profiles(request)
    
    cleaner = forms.CharField()
    upk = cleaner.clean(upk)
    
    #delete the UserProfile
    user_to_delete = UserProfile.objects.get(user=upk)
    user_to_delete.delete()
    
    #delete the Django User
    user_to_delete = User.objects.get(id=upk)
    user_to_delete.delete()
    
    return profiles(request)
    
    
@login_required
def view(request, upk): 
    context = {}
    context['alert_count'] = Alerts.objects.filter(soft_delete=False).count()
    cleaner = forms.CharField()
    upk = cleaner.clean(upk)
    
    user_data = UserProfile.objects.get(user=upk)
    context['user_data'] = user_data
    context['can_edit'] = False
    
    return render(request, 'accounts/view_profile.html', context)
    
    
@login_required
def create(request): 
    context = {}
    context['alert_count'] = Alerts.objects.filter(soft_delete=False).count()
    
    cleaner = forms.CharField()
    context['utc_offsets'] = utc_offsets
    
    #check if the current user is allowed to create new users
    this_profile = UserProfile.objects.get(user = request.user)
    if this_profile.oauth_scope == 'read write':
        context['can_edit'] = True
    else:
        return profiles(request)
    
    if request.method == "POST":
            
        user_profile_create_form = UserProfileEditForm(request.POST)
        user_create_form = UserEditForm(request.POST, instance=request.user)
        if user_create_form.is_valid() and user_profile_create_form.is_valid():
            context['edit_msg'] = " New User successfully created."
            
            #get new django user from POST data
            username = cleaner.clean(request.POST['username'])
            first_name = user_create_form.cleaned_data.get("first_name")
            last_name = user_create_form.cleaned_data.get("last_name")
            email = user_create_form.cleaned_data.get("email")
            pw1 = cleaner.clean(request.POST['inputpassword1']) 
            pw2 = cleaner.clean(request.POST['inputpassword2'])
            
            if pw1 == pw2:
                #passwords match so create new user
                new_user = User(username=username,
                                first_name=first_name,
                                last_name=last_name,
                                email=email,
                               )
                new_user.set_password(pw1)               
                new_user.save()
                
                oauth_scope = user_profile_create_form.cleaned_data.get("oauth_scope")
                utc_offset = user_profile_create_form.cleaned_data['utc_offset']
                new_user_profile = UserProfile(user=new_user,
                                               oauth_scope=oauth_scope,
                                               utc_offset=utc_offset
                                               )
                new_user_profile.save()                               
            
            return profiles(request) 
            
        else:
          context['edit_msg'] = "Received data is not valid." 
          return render(request, 'accounts/create_profile.html', context)
        
    return render(request, 'accounts/create_profile.html', context)    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
