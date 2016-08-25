#
# Authors: Robert Abram <robert.abram@entpack.com>
#
# Copyright (C) 2015 EntPack
# see file 'COPYING' for use and warranty information
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
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django import forms
from django.db.models import Q 
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
from rest_framework import permissions, viewsets
from rest_framework.decorators import list_route
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from proj.serializer import RecordCountSerializer
from apps.rules.serializers import *
from apps.rules.models import *
from apps.accounts.models import UserProfile
from apps.rules.iptables.models import *
from apps.alerts.models import *
from proj.models import RecordCount, ChooserList


# ---- Start Prototype UI code ----- #

@login_required
def bundles(request):
    context = {}
    context['alert_count'] = Alerts.objects.filter(soft_delete=False).count()
    context['module'] = 'bundles'
    bundle_results = None
    
    this_user = UserProfile.objects.get(user=request.user)
    if 'write' in this_user.oauth_scope.split():
        context['can_edit'] = True
        if request.method == "POST":
            txt_cleaner = forms.CharField()
            txt_cleaner.required = False
            search_term = txt_cleaner.clean(request.POST.get('search_term',''))
            bundle_results = Bundle.objects.filter(Q(descr__icontains=search_term) | Q(name__icontains=search_term))
 
        else:    
        # There's no POST data so get all the bundles
            bundle_results = Bundle.objects.all()
    
    # record how many chains are in each bundle
    counts = []
    for bundle in bundle_results:
        if bundle.platform == 'iptables':
            bundle_count = IPTablesMachineSet.objects.filter(bundle=bundle).count()
        counts.append([bundle.id, bundle_count])
        
    context['counts'] = counts    
    context['all_bundles'] = bundle_results 

    return render(request, 'rules/bundles.html', context )
    
@login_required
def create_bundle(request):
    context = {}
    context['alert_count'] = Alerts.objects.filter(soft_delete=False).count()
    
    context['platforms'] = RULE_PLATFORMS
    
    #get allowable chains
    chains = IPTablesMachineSubset.objects.all() 
    context['chains'] = chains
  
    this_user = UserProfile.objects.get(user=request.user)
    if 'write' in this_user.oauth_scope.split():
        context['can_edit'] = True  
        
        if request.method == "POST":
            # new bundle data has been recieved so create the new bundle
            txt_cleaner = forms.CharField()
            
            # get incoming form data
            bundle_name = txt_cleaner.clean(request.POST.get('bundle_name',''))
            description = txt_cleaner.clean(request.POST.get('description',''))
            platform = txt_cleaner.clean(request.POST.get('platform',''))
            notes = txt_cleaner.clean(request.POST.get('notes',''))

            # create the new bundel from form data
            new_bundle = Bundle( 
                                  name=bundle_name,
                                  platform=platform.lower(),
                                  default=False,
                                  descr=description,
                                  notes=notes,
                                )  # only one machine_subset can be active at a time 
                                             
            new_bundle.save()

            # Auto add all administrative, logging and rejection rules.
            for slot, name in RULE_MACHINE_SUBSET_SLOTS:
                if slot == 110 or slot >= 9800:
                    # Assume there will be more than one record returned, just add them all.
                    for mss in IPTablesMachineSubset.objects.filter(platform=new_bundle.platform, slot=slot):
                        IPTablesMachineSet(machine_subset=mss, bundle=new_bundle, enabled=True).save()

            return redirect('/rules/iptables/bundles/bundle/{0}/edit/'.format(new_bundle.id))
  
    return render(request, 'rules/create_bundle.html', context)


@login_required
def machine_subsets(request):
    context = {}
    context['alert_count'] = Alerts.objects.filter(soft_delete=False).count()
    
    all_machine_subsets = None
    this_user = UserProfile.objects.get(user=request.user)
    if 'write' in this_user.oauth_scope.split():
        context['can_edit'] = True
        if request.method == "POST":
            txt_cleaner = forms.CharField()
            txt_cleaner.required = False
            search_term = txt_cleaner.clean(request.POST.get('search_term',''))
            if search_term != '':
                all_machine_subsets = IPTablesMachineSubset.objects.filter( Q(descr__icontains=search_term) | 
                                                                            Q(name__icontains=search_term) 
                                                                          ).order_by('slot')
                
                #jump through a lot of hoops to search the slot names                                      
                all_slots_by_text = []
                slots_by_number = []                                                          
                for slot in RULE_MACHINE_SUBSET_SLOTS:
                    all_slots_by_text.append(slot[1])
                    
                matching_slots = [s for s in all_slots_by_text if search_term in s]
                
                for slot_text in matching_slots :
                    for slot in RULE_MACHINE_SUBSET_SLOTS:
                        if slot_text == slot[1]:
                            slots_by_number.append(slot[0])
                
                machine_subsets_by_matching_slot = IPTablesMachineSubset.objects.filter(slot__in=slots_by_number)
                
                
                #finally combine all search results together
                all_machine_subsets = chain(all_machine_subsets, machine_subsets_by_matching_slot)
            else:
                # there's no search term so list all the machine subsets
                all_machine_subsets = IPTablesMachineSubset.objects.all().order_by('slot')    
        else:    
        # There's no POST data so get all the machine subsets
            all_machine_subsets = IPTablesMachineSubset.objects.all().order_by('slot')
    
    
    context['all_machine_subsets'] = all_machine_subsets
    return render(request, 'rules/machine_subsets.html', context)

# ---- End Prototype UI code ----- #

# ---- Start API code -------------#


# ---------------------------------#
# Model Chooser List ViewSets
# ---------------------------------#

class BundleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Node Model View Set
    """
    queryset = Bundle.objects.all()
    serializer_class = BundleSerializer

    # Return the Bundle model record count
    @list_route(['get'])
    def count(self, request):
        count = RecordCount(Bundle.objects.count())
        serializer = RecordCountSerializer(count)
        self.renderer_classes = (JSONRenderer, BrowsableAPIRenderer,)
        return Response(serializer.data)

    def get_queryset(self):
        """
        Allow filtering by default and name
        """
        queryset = Bundle.objects.all()

        default = self.request.query_params.get('default', None)
        if default is not None:
            queryset = queryset.filter(default=True)

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)

        return queryset


class RulePlatformViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = []

    for (code, desc) in RULE_PLATFORMS:
        queryset.append(ChooserList(len(queryset)+1, code, desc))

    serializer_class = RulePlatformListSerializer
    resource_name = "rule-platform"


class MachineSubsetSlotsViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = []

    for (code, desc) in RULE_MACHINE_SUBSET_SLOTS:
        queryset.append(ChooserList(len(queryset) + 1, code, desc))

    serializer_class = MachineSubsetSlotsListSerializer
    resource_name = "machine_subset-slots"
    
    


# ---- End API code ---------------#
