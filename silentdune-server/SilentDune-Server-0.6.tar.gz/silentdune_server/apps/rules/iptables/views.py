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

import logging
import string
import random
import collections
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django import forms 
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.core.validators import ValidationError

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
from rest_framework import permissions, viewsets
from rest_framework.decorators import list_route
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response

from apps.rules.iptables.models import *
from apps.alerts.models import *
from apps.rules.models import Bundle, RULE_MACHINE_SUBSET_SLOTS, RULE_PLATFORMS
from apps.node.models import NodeBundle, Node
from apps.accounts.models import UserProfile
from proj.mixins import *
from proj.models import RecordCount, ChooserList
from proj.serializer import RecordCountSerializer, ChooserListBaseSerializer
#from proj.views import BaseCreateListUpdateDestroyAPIView, BaseListAPIView
from .serializers import *

logger = logging.getLogger(__name__)


               
jump_target_icons={"DROP":["DROP", "glyphicon-remove-circle", "red"], "ACCEPT":["ACCEPT", "glyphicon-ok-circle", "green"], 
                   "LOG":["LOG", "glyphicon-exclamation-sign","blue"], "REJECT (IPV4)":["REJECT (IPV4)", "glyphicon-ban-circle", "red"], 
                   "REJECT (IPV6)":["REJECT (IPV6)", "glyphicon-ban-circle", "red"]}                                  
    
# utility functions

def prefix_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



# ---- Start Prototype UI code ----- #

@login_required
def bundles(request):

    return render(request, 'iptables/bundles.html', {'module': 'bundles'})


@login_required
def edit_bundle(request, id):
    panels = ['success','info','warning','danger']
    context = {}
    context['alert_count'] = Alerts.objects.filter(soft_delete=False).count()
    this_bundle = Bundle.objects.get(id = id)
    
    this_user = UserProfile.objects.get(user=request.user)
    if 'write' in this_user.oauth_scope.split():
        context['can_edit'] = True
    
        if request.method == "POST":
            cleaner = forms.CharField()
            this_bundle = None
            #reset all machine_set 'enabled' values to 0
            clean_bundle_id = cleaner.clean(request.POST['bundle_id'])
            if clean_bundle_id == id :
                this_bundle = Bundle.objects.get(id = clean_bundle_id)
                machine_sets = IPTablesMachineSet.objects.filter(bundle=this_bundle)
                for machine_set in machine_sets:
                    machine_set.enabled = 0
                    machine_set.save()
                    
                    
            
            #reassert machine_set 'enabled' for those that are checked            
            for item in request.POST:
                this_item = cleaner.clean(item)            
                if this_item.find('chain_') != -1:
                    machine_subset_id = this_item[6:]
                    this_machine_subset = IPTablesMachineSubset.objects.get(id=machine_subset_id)
                    this_machine_set = IPTablesMachineSet.objects.get(machine_subset=this_machine_subset, bundle=this_bundle) 
                    this_machine_set.enabled = True
                    this_machine_set.save()
            
            # if a new machine subset has been added create the many-to-many link here 
            machine_subset = request.POST.get('machine_subset', '')
            
            if machine_subset != "" : 
                machine_subset = cleaner.clean(request.POST['machine_subset'])
            
                if machine_subset in IPTablesMachineSubset.objects.values_list('name', flat=True) :
                  
                    machine_subset_enabled = request.POST.get('machine_subset_enabled', '')
                    if machine_subset_enabled != "":
                        machine_subset_enabled = cleaner.clean(request.POST['machine_subset_enabled'])
                        
                    machine_subset_enabled = True if( machine_subset_enabled == 'on' ) else False              
                    
                    new_machine_set = IPTablesMachineSet(
                                               machine_subset=IPTablesMachineSubset.objects.get(name=machine_subset),
                                               bundle=this_bundle,
                                               enabled=machine_subset_enabled 
                                             ) 
                                                         
                    new_machine_set.save() 
                    
            # save new bundle values        
            name = cleaner.clean(request.POST.get('name',''))
            this_bundle.name = name
            cleaner.required = False
            descr = cleaner.clean(request.POST.get('desc',''))
            this_bundle.descr = descr
            notes = cleaner.clean(request.POST.get('notes',''))
            this_bundle.notes = notes
            this_bundle.save()
    
    all_bundle_node_ids = []
    these_bundlenodes = NodeBundle.objects.filter(bundle=this_bundle)
    
    for bundlenode in these_bundlenodes:
        all_bundle_node_ids.append(bundlenode.node.id)
                    
    all_bundle_nodes = Node.objects.filter(id__in=all_bundle_node_ids)
    node_locked_count = all_bundle_nodes.filter(locked=True).count()
    this_bundle.locked_count = node_locked_count
    this_bundle.total_count = all_bundle_nodes.count()
    
    
    context['bundle'] = this_bundle 
    
    machine_sets = IPTablesMachineSet.objects.filter(bundle=this_bundle)
    machine_subset_ids = []
    for machine_set in machine_sets:
        machine_subset_ids.append(machine_set.machine_subset_id)
        
    #get all the machine_subsets    
    all_machine_subsets = IPTablesMachineSubset.objects.filter(id__in=machine_subset_ids)
    available_machine_subsets = IPTablesMachineSubset.objects.all()
    
    #get the unique slots used by this group of machine_subsets
    all_slots = all_machine_subsets.values_list('slot', flat=True)
    unique_slots = sorted(set(all_slots))
    
    #create grouping of machine subsets by function (ie slot) for human readable text
    machine_subset_groups = []
    for idx, this_slot in enumerate(unique_slots):
        this_machine_subset = {}
        this_machine_subset['sets'] = []
        
        #rotate through BootStrap panel types (colors)
        this_machine_subset['panel'] = panels[idx%len(panels)] 
         
        the_machine_subsets = all_machine_subsets.filter(slot = this_slot)
        for machine_subset in the_machine_subsets:
            #create the list of available machine subsets by removing already included machine subsets from the global list
            available_machine_subsets = available_machine_subsets.exclude(id = machine_subset.id)
            
            #add the 'enabled' state to the machine subset that is active
            subset_enabled = IPTablesMachineSet.objects.get(machine_subset=machine_subset, bundle=this_bundle).enabled           
            this_machine_subset['sets'].append((machine_subset, subset_enabled))
        for the_slot in RULE_MACHINE_SUBSET_SLOTS:
            if the_slot[0] == this_slot:
                this_machine_subset['name'] = the_slot[1]   

        machine_subset_groups.append(this_machine_subset)
        
    # pass available machine subsets to the template    
    context['available_machine_subsets'] = available_machine_subsets    
    
    # pass active machine subets, ordered by group to the template 
    context['machine_subset_groups'] = machine_subset_groups
    
    return render(request, 'iptables/edit_bundle.html', context )


@login_required
def view_bundle(request, id):
    panels = ['success','info','warning','danger']
    context = {}
    context['alert_count'] = Alerts.objects.filter(soft_delete=False).count()
    
    this_bundle = Bundle.objects.get(id = id)
    
    context['bundle'] = this_bundle 
    
    machine_sets = IPTablesMachineSet.objects.filter(bundle=this_bundle)
    machine_subset_ids = []
    for machine_set in machine_sets:
        machine_subset_ids.append(machine_set.machine_subset_id)
        
    #get all the machine_subsets    
    all_machine_subsets = IPTablesMachineSubset.objects.filter(id__in=machine_subset_ids)
    available_machine_subsets = IPTablesMachineSubset.objects.all()
    
    #get the unique slots used by this group of machine_subsets
    all_slots = all_machine_subsets.values_list('slot', flat=True)
    unique_slots = sorted(set(all_slots))
    
    #create grouping of machine subsets by function (ie slot) for human readable text
    machine_subset_groups = []
    for idx, this_slot in enumerate(unique_slots):
        this_machine_subset = {}
        this_machine_subset['sets'] = []
        
        #rotate through BootStrap panel types (colors)
        this_machine_subset['panel'] = panels[idx%len(panels)] 
         
        the_machine_subsets = all_machine_subsets.filter(slot = this_slot)
        for machine_subset in the_machine_subsets:
            #create the list of available machine subsets by removing already included machine subsets from the global list
            available_machine_subsets = available_machine_subsets.exclude(id = machine_subset.id)
            
            #add the 'enabled' state to the machine subset that is active
            subset_enabled = IPTablesMachineSet.objects.get(machine_subset=machine_subset, bundle=this_bundle).enabled           
            this_machine_subset['sets'].append((machine_subset, subset_enabled))
        for the_slot in RULE_MACHINE_SUBSET_SLOTS:
            if the_slot[0] == this_slot:
                this_machine_subset['name'] = the_slot[1]   

        machine_subset_groups.append(this_machine_subset)    
 
         
    context['available_machine_subsets'] = available_machine_subsets    
    context['machine_subset_groups'] = machine_subset_groups
    
    return render(request, 'iptables/edit_bundle.html', context )


@login_required
def delete_bundle(request, id):
    
    result = Bundle.objects.filter(id=id).delete()

    return redirect('/rules/bundles/')

 
    
    
@login_required
def view_machine_subset(request, machine_subset_id):
    context = {}
    context['can_edit'] = False
    context['alert_count'] = Alerts.objects.filter(soft_delete=False).count()
    
    # Prepare machine_subset data for display in the template
    this_machine_subset = IPTablesMachineSubset.objects.get(id=machine_subset_id)
    
    chains = IPTablesChain.objects.filter(machine_subset=this_machine_subset)
    rings = IPTablesRing.objects.filter(chain__in=chains)
    rules = IPTablesRule.objects.filter(ring__in=rings).order_by('sort_id')
    
    context['machine_subset'] = this_machine_subset
    context['chains'] = []
    
    for chain in chains:
        chain_rings = []
        for ring in rings:
            ring_rules = []
            if ring.chain == chain:
                for rule in rules:
                    if rule.ring == ring:
                        ring_rules.append(rule)
                chain_rings.append({'name': ring.name, 'id': ring.id, 'rules': ring_rules})
        context['chains'].append({'name': chain.name, 'id': chain.id, 'rings' : chain_rings})      
        
    return render(request, 'iptables/edit_machine_subset.html', context)     

@login_required
def edit_machine_subset(request, machine_subset_id):
    context = {}
    context['alert_count'] = Alerts.objects.filter(soft_delete=False).count()
    
    this_user = UserProfile.objects.get(user=request.user)
    if 'write' in this_user.oauth_scope.split():
        context['can_edit'] = True
        if request.method == "POST":
            txt_cleaner = forms.CharField()
            
            chain_name = txt_cleaner.clean(request.POST.get('name',''))
            chain_descr = txt_cleaner.clean(request.POST.get('descr',''))
            chain_notes = txt_cleaner.clean(request.POST.get('notes',''))
            chain_id = txt_cleaner.clean(request.POST.get('chain_id',''))
            
            this_machine_subset = IPTablesMachineSubset.objects.get(id=chain_id)
            
            this_machine_subset.name = chain_name
            this_machine_subset.descr = chain_descr
            this_machine_subset.notes = chain_notes
            
            if int(request.session['edit_machine_subset_id']) == int(chain_id):
                #check that the machine subset id has not been tampered with
                this_machine_subset.save()
            else:
                #TODO: if id's don't match then log it here.
                pass
 
        
    # Prepare machine_subset data for display in the template   
    this_machine_subset = IPTablesMachineSubset.objects.get(id=machine_subset_id)
    request.session['edit_machine_subset_id'] = this_machine_subset.id 
    
    chains = IPTablesChain.objects.filter(machine_subset=this_machine_subset)
    rings = IPTablesRing.objects.filter(chain__in=chains)
    rules = IPTablesRule.objects.filter(ring__in=rings).order_by('sort_id')
    
    context['machine_subset'] = this_machine_subset
    context['chains'] = []
    
    for chain in chains:
        chain_rings = []
        for ring in rings:
            ring_rules = []
            if ring.chain == chain:
                for rule in rules:
                    if rule.ring == ring:
                        jump_option = IPTablesJump.objects.get(rule=rule)
                        if jump_option.target.upper() in ('LOG', 'ACCEPT', 'REJECT (IPV4)', 'REJECT (IPV6)', 'DROP'):
                            rule.jump_target = jump_target_icons[jump_option.target.upper()]
                        else:
                            rule.jump_target = [ jump_option.target.upper(), "glyphicon-record","orange"]
                        ring_rules.append(rule)
                chain_rings.append({'name': ring.name, 'id': ring.id, 'rules': ring_rules})
        context['chains'].append({'name': chain.name, 'id': chain.id, 'rings' : chain_rings})
    
    request.session['edit_machine_subset_id'] = this_machine_subset.id    
    #print("data", context['chains']) 
    
    context['edit'] = True         
        
    return render(request, 'iptables/edit_machine_subset.html', context)
    
    
@login_required
def create_machine_subset(request):
    context = {}
    context['alert_count'] = Alerts.objects.filter(soft_delete=False).count()
    
    context['slots'] = RULE_MACHINE_SUBSET_SLOTS   
    context['platforms'] = RULE_PLATFORMS
    
    this_user = UserProfile.objects.get(user=request.user)
    if 'write' in this_user.oauth_scope.split():
        context['can_edit'] = True
        
        if request.method == "POST":
            #machine_subset data has been recieved so create the new machine_subset
            txt_cleaner = forms.CharField()
            
            chain_name = txt_cleaner.clean(request.POST.get('chain_name',''))
            
            # if the new chain name already exists then return to create machine subset
            name_exists = IPTablesMachineSubset.objects.filter(name=chain_name).count()
            if name_exists > 0:
                return redirect('/rules/iptables/machine_subset/create/')
                
            platform = txt_cleaner.clean(request.POST.get('platform',''))
            slot = txt_cleaner.clean(request.POST.get('slots',''))
            description = txt_cleaner.clean(request.POST.get('desc',''))
            notes = txt_cleaner.clean(request.POST.get('notes',''))
            
            #convert slot value from text to numeric
            for pair in RULE_MACHINE_SUBSET_SLOTS:
                if pair[1] == slot:
                    slot = pair[0]
            
            new_machine_subset = IPTablesMachineSubset( 
                                              name=chain_name,
                                              platform=platform.lower(),
                                              slot=slot,
                                              descr=description,
                                              notes=notes,
                                              sort_id=9992
                                             )  # new machine_subsets are inactive by default 
                                             
            new_machine_subset.save() 
            
            if txt_cleaner.clean(request.POST.get('rule','')) == 'true':
                return redirect('/rules/iptables/rules/rule/create/0/'+str(new_machine_subset.id)+'/')
            
    return render(request, 'iptables/create_machine_subset.html', context)    

 


@login_required
def delete_machine_subset(request, machine_subset_id):
    # delete this machine_subset and all objects that reference it
    result = IPTablesMachineSubset.objects.filter(id=machine_subset_id).delete()
    
    return redirect('/rules/machine_subsets/')
    

    
    

    
    
@login_required
def create_rule(request, ring_id='0', machine_subset_id='0'):
    context = {}
    context['alert_count'] = Alerts.objects.filter(soft_delete=False).count()
    
    context['slots'] = RULE_MACHINE_SUBSET_SLOTS   
    context['platforms'] = RULE_PLATFORMS
    context['function'] = "Create"
    context['match_fields'] = IPTablesMatch.match_fields 
    context['jump_fields'] = IPTablesJump.jump_fields
    context['mask'] = reversed(range(1,32))
    context['mask2'] = reversed(range(1,32)) # have to redo this from some weird reason. page will not populate without it.
    
    this_ring = None
    this_chain = None
    sort_id = 1
    
    if ring_id != '0':
        #collect the known default values for this chain and pass to the template
        this_ring = IPTablesRing.objects.get(id = ring_id)
        this_chain = IPTablesChain.objects.get(id = this_ring.chain_id)
        this_machine_subset = IPTablesMachineSubset.objects.get(id = this_chain.machine_subset_id)
        context['transport'] =  this_ring.version
        context['table'] = this_chain.name    
        context['chain'] = this_ring.name
        context['rule_edit'] = False
        context['chain_id'] = this_chain.id
        context['machine_subset_id'] = this_machine_subset.id
        
        # get the value of the next sort id 
        rules_by_sort_id = IPTablesRule.objects.filter(ring_id = ring_id).order_by('-sort_id')
        
        # if there are rules that reference this ring then get their sort id
        if len(rules_by_sort_id) != 0:
            sort_id = rules_by_sort_id[0].sort_id + 1
        #print("sort id: ", rules_by_sort_id[0].sort_id )
        
        
    elif machine_subset_id != '0':    
        # No existing ring so save the id for after the post
        request.session['machine_subset_id'] = machine_subset_id
        context['machine_subset_id'] = machine_subset_id 
        
        
    this_user = UserProfile.objects.get(user=request.user)
    if 'write' in this_user.oauth_scope.split():
        context['can_edit'] = True
        
        if request.method == "POST":
            #rule data has been recieved so create the new rule
            txt_cleaner = forms.CharField()
            ip_cleaner = forms.GenericIPAddressField()
            
            # get the posted data for the Rule edit
            transport = txt_cleaner.clean( request.POST['transport'] )
            enabled = txt_cleaner.clean( request.POST['enabled'] )
            txt_cleaner.required = False
            description = txt_cleaner.clean( request.POST['description'] )
            protocol = txt_cleaner.clean( request.POST['protocol'] )
            table = txt_cleaner.clean( request.POST['table'] )
            chain = txt_cleaner.clean( request.POST['chain'] )
            ifacein = txt_cleaner.clean( request.POST['ifacein'] )
            ifaceout = txt_cleaner.clean( request.POST['ifaceout'] )
            source_address = txt_cleaner.clean( request.POST['source-address'] )
            source_mask = txt_cleaner.clean( request.POST['source-mask'] )
            dest_address = txt_cleaner.clean( request.POST['dest-address'] )
            dest_mask = txt_cleaner.clean( request.POST['dest-mask'] )
            
            if source_mask in ( '','None')  :
                source_mask = None
            else:
                source_mask = int(source_mask)    
                
            if dest_mask in ( '', 'None'):
                dest_mask = None
            else:
                dest_mask = int(dest_mask)                
            
            
            
            if request.session.get('machine_subset_id', None) != None:
                #machine_subset id has been stored so there's a machine_subset but no ring or chain.
                #create them here
                
                new_chain = IPTablesChain(
                                             machine_subset=IPTablesMachineSubset.objects.get(id=request.session['machine_subset_id']),
                                             name=table.lower()
                                         )
                new_chain.save()                         
                                         
                new_ring = IPTablesRing(
                                           chain=new_chain,
                                           name=chain.lower(),
                                           version=transport.lower()
                                       )
                new_ring.save()
                this_ring = new_ring
                                       
                request.session['machine_subset_id'] = None                        
                       
            
            # create the new rule 
            #created_edited_rule = IPTablesRule.objects.get(id=id_in)
            #if this_ring is None: this_ring = 0
            enabled = True if( enabled == 'Enabled' ) else False #cheezy syntax but works
            #print("sort: ", type( sort_id), " source", type(source_mask), " dest", type(dest_mask) )
            created_edited_rule = IPTablesRule(
                                                # assign posted values to the rule
                                                 ring = this_ring, 
                                                 enabled = enabled,
                                                 descr = description,
                                                 ip_protocol_name = protocol , 
                                                 ifacein_name = ifacein,
                                                 ifaceout_name = ifaceout, 
                                                 source_address = source_address,  
                                                 source_mask = source_mask,
                                                 dest_address = dest_address, 
                                                 dest_mask = dest_mask,
                                                 sort_id = sort_id,
                                                
                                                #reset 'invert' booleans
                                                 ifacein_invert = False,
                                                 ifaceout_invert = False,
                                                 ip_protocol_invert = False,
                                                 source_invert = False,
                                                 dest_invert = False
                                              )
            created_edited_rule.save()    
                             
            #set the 'inverts' that are checked on the rule edit page
            if  request.POST.get('ifacein_invert'):
                created_edited_rule.ifacein_invert = True
            if  request.POST.get('ifaceout_invert'):
                created_edited_rule.ifaceout_invert = True 
            if  request.POST.get('protocol_invert'):
                created_edited_rule.ip_protocol_invert = True
            if  request.POST.get('source_invert'):
                created_edited_rule.source_invert = True
            if  request.POST.get('dest_invert'):
                created_edited_rule.dest_invert = True                                                   
                
            # save the new values for the rule being edited    
            created_edited_rule.save()
            
            
            # deal with jumps and matches here
            
            # create a default Jump Target for this rule
            default_jump = IPTablesJump(rule=created_edited_rule,
                                        target='Accept')
            default_jump.save()
            
            rule_id = created_edited_rule.id
            form_prefixes_and_ids = request.session['form_prefixes_and_ids']
            # save match and match options data
            form_prefixes_and_ids = request.session['form_prefixes_and_ids']
            IPTablesMatch.save_matches(request.POST, form_prefixes_and_ids, rule_id)
 
            #save jump options data
            IPTablesJumpOptions.save_options(request.POST, rule_id)                                                    
            
    #context['total_matches'] = total_matches
    #context['total_options'] = total_options 
    
    context['total_matches'] = 0
    context['total_options'] = 0                         
            
    return render(request, 'iptables/edit_create_rule.html', context)     


@login_required
def edit_rule(request, rule_id):
    context = {}
    context['alert_count'] = Alerts.objects.filter(soft_delete=False).count()
    
    context['rule_edit'] = True
    context['function'] = "Edit" 
    context['match_fields'] = IPTablesMatch.match_fields   
    context['jump_fields'] = IPTablesJump.jump_fields
    context['mask'] = reversed(range(1,32))
    context['mask2'] = reversed(range(1,32))
    
    this_user = UserProfile.objects.get(user=request.user)
    
    if 'write' in this_user.oauth_scope.split():
        context['can_edit'] = True  
          
        if request.method == "POST":
            # save Rule data          
            IPTablesRule.edit(request.POST, rule_id)
 
            # save match and match options data
            form_prefixes_and_ids = request.session['form_prefixes_and_ids']
            IPTablesMatch.save_matches(request.POST, form_prefixes_and_ids, rule_id)
 
            #save jump options data
            IPTablesJumpOptions.save_options(request.POST, rule_id) 
             
    this_rule = IPTablesRule.objects.get(id=rule_id)
    machine_subset_id = this_rule.ring.chain.machine_subset.id
    transport = this_rule.ring.version
    table = this_rule.ring.chain.name
    chain = this_rule.ring.name
    
    all_matches = IPTablesMatch.objects.filter(rule=this_rule).order_by('name') 
    all_options = IPTablesMatchOptions.objects.filter(match_name__in=all_matches)
    
    the_jump = IPTablesJump.objects.get(rule=this_rule)
    all_jump_options = IPTablesJumpOptions.objects.filter(jump=the_jump)
    
    form_prefixes_and_ids = []
    
    for match in all_matches:
        prefix = prefix_generator()
        form_prefixes_and_ids.append( [prefix, match.id] )
        match.prefix = prefix
 
        
    request.session['form_prefixes_and_ids'] = form_prefixes_and_ids       
        
    
    total_matches = all_matches.count()
    total_options = all_options.count()
    
    if this_rule.enabled:
        this_rule.enabled = "Enabled"
    else:
        this_rule.enabled = "Disabled"
        
    if this_rule.source_mask == None: this_rule.source_mask = ''
    if this_rule.dest_mask == None: this_rule.dest_mask = ''    
        
        
    context['rule'] = this_rule
    context['transport'] = transport
    context['chain'] = chain
    context['table'] = table
    context['machine_subset_id'] = machine_subset_id
    context['matches'] = all_matches
    context['jump_target'] = the_jump.target
    context['jump_options'] = all_jump_options
    context['total_matches'] = total_matches
    context['total_options'] = total_options
    return render(request, 'iptables/edit_create_rule.html',  context)
    
    
@login_required
def delete_rule(request, rule_id):
    context = {}
    
    # Get the machine_subset id for redirect
    this_rule = IPTablesRule.objects.get(id=rule_id)
    this_ring = IPTablesRing.objects.get(id=this_rule.ring_id)
    this_chain = IPTablesChain.objects.get(id=this_ring.chain_id)
    this_machine_subset = IPTablesMachineSubset.objects.get(id=this_chain.machine_subset_id)
    
    # Delete the rule
    result = IPTablesRule.objects.filter(id=rule_id).delete()
    
    # if there are no other rules under this ring then delete it
    ring_rule_count = IPTablesRule.objects.filter(ring=this_ring).count()
    if ring_rule_count == 0:
        result = IPTablesRing.objects.filter(id=this_ring.id).delete()
    
    # if there are no other rings under this chain then delete it    
    chain_ring_count = IPTablesRing.objects.filter(chain=this_chain).count()
    if chain_ring_count == 0:
        result = IPTablesChain.objects.filter(id=this_chain.id).delete()        
        
        
    
    return redirect('/rules/iptables/machine_subset/'+str(this_machine_subset.id)+'/edit/')

# ---- End Prototype UI code ----- #

# ---- Start API code -------------#


@require_http_methods(["POST", "GET"])
def enable(request):  
    rule_id = request.POST['rule_id']  
    enabled = request.POST['enabled']
    
    #convert text to boolean
    if enabled == "true":
        enabled = True
    else:
        enabled = False
        
    #update the rules 'enabled' state    
    this_rule = IPTablesRule.objects.get(id = rule_id)
    this_rule.enabled = enabled
    this_rule.save()
      
    return HttpResponse("Success")
    
    
    
@require_http_methods(["POST", "GET"])
def move_rule(request): 
    # the position of a rule in a ring has been changed at the UI
    # reflect that change here in the database by updating sort_id's
  
    rule_id = request.POST['rule_id']  
    up = request.POST['up']
    
    this_rule = IPTablesRule.objects.get(id = rule_id)
    
    # get all rules in the same ring
    all_rules_in_ring = IPTablesRule.objects.filter(ring_id = this_rule.ring_id).order_by('sort_id')

    # update the sort orders
    this_sort_id = this_rule.sort_id
    if up == 'true':
        # get the rule above
        swap_rule = all_rules_in_ring.get(sort_id = this_sort_id - 1)
    elif up == 'false':
        # get the rule below
        swap_rule = all_rules_in_ring.get(sort_id = this_sort_id + 1)
      
    this_rule.sort_id = swap_rule.sort_id
    swap_rule.sort_id = this_sort_id
    this_rule.save()
    swap_rule.save()     
  
    return HttpResponse("Success")    
    
@require_http_methods(["POST", "GET"])
def alter_bundle_nodes(request):
    
    #print("doing shutdown")
    bundle_id = request.POST['bundle_id']
    parameter = request.POST['parameter']
    
    this_bundle = Bundle.objects.get(id=bundle_id)
    all_bundle_node_ids = []
    these_bundlenodes = NodeBundle.objects.filter(bundle=this_bundle)
    
    for bundlenode in these_bundlenodes:
        all_bundle_node_ids.append(bundlenode.node.id)
                    
    all_bundle_nodes = Node.objects.filter(id__in=all_bundle_node_ids)
    
    for node in all_bundle_nodes:
        if parameter == "lock_all":
            node.locked = True
        elif parameter == "unlock_all":
            node.locked = False
        
        node.sync = True    
        node.save()      
    
    print("doing shutdown. bundle id:", bundle_id," parameter", parameter)
    
  
    return HttpResponse("Success")      
    
    
    


class IPRingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rings to be viewed or edited.
    """
    queryset = IPTablesRing.objects.all()
    serializer_class = IPRingSerializer

    # Return the record count
    @list_route(['get'])
    def count(self, request):
        count = RecordCount(IPTablesRing.objects.count())
        serializer = RecordCountSerializer(count)
        self.renderer_classes = (JSONRenderer, BrowsableAPIRenderer,)
        return Response(serializer.data)


class IPRuleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rings to be viewed or edited.
    """
    queryset = IPTablesRule.objects.all()
    serializer_class = IPRuleSerializer

    # Return the record count
    @list_route(['get'])
    def count(self, request):
        count = RecordCount(IPTablesRule.objects.count())
        serializer = RecordCountSerializer(count)
        self.renderer_classes = (JSONRenderer, BrowsableAPIRenderer,)
        return Response(serializer.data)

    def get_queryset(self):
        """
        Queryset is always filtered by ring id portion of the URL.
        """
        return IPTablesRule.objects.filter(ring=self.kwargs['ring'])


class IPChainViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows chains to be viewed or edited.
    """
    queryset = IPTablesChain.objects.all()
    serializer_class = IPChainSerializer

    # Return the record count
    @list_route(['get'])
    def count(self, request):
        count = RecordCount(IPTablesChain.objects.count())
        serializer = RecordCountSerializer(count)
        self.renderer_classes = (JSONRenderer, BrowsableAPIRenderer,)
        return Response(serializer.data)

    def get_queryset(self):
        """
        Queryset is always filtered by chain id portion of the URL.
        """
        return IPTablesChain.objects.filter(machine_subset=self.kwargs['set'])


class IPMachineSubsetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows chains to be viewed or edited.
    """
    queryset = IPTablesMachineSubset.objects.all()
    serializer_class = IPMachineSubsetSerializer

    @list_route()
    def machine_subsetnamelist(self, request):
        self.serializer_class = IPMachineSubsetNameListSerializer
        return super(IPMachineSubsetSerializer, self).list(self, request)

    # Return the record count
    @list_route(['get'])
    def count(self, request):
        count = RecordCount(IPTablesMachineSubset.objects.count())
        serializer = RecordCountSerializer(count)
        self.renderer_classes = (JSONRenderer, BrowsableAPIRenderer,)
        return Response(serializer.data)


class IPMachineSetViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = IPTablesMachineSet.objects.all()
    serializer_class = IPMachineSetSerializer

    def get_queryset(self):
        """
        Queryset is always filtered by bundle id portion of the URL.
        """
        return IPTablesMachineSet.objects.filter(bundle=self.kwargs['bundle'])
        
        
       


# ---------------------------------#
# Model Chooser List ViewSets
# ---------------------------------#

# IPTransportVersionViewSet does not use the IPBaseChooserListViewSet because the code value is an Integer
class IPTransportVersionViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = IPTransportVersionListSerializer

    def __init__(self):

        self.resource_name = 'transport-version'
        self.queryset = []

        for (code, desc) in IPTABLES_TRANSPORT_VERSION:
            self.queryset.append(ChooserList(len(self.queryset)+1, code, desc))


class IPBaseChooserListViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = ChooserListBaseSerializer

    def __init__(self, data, resource_name, **kwargs):
        # RequestLogViewMixin.__init__(self)
        # BaseListAPIView.__init__(self, **kwargs)

        self.resource_name = resource_name
        self.queryset = []

        for (code, desc) in data:
            self.queryset.append(ChooserList(len(self.queryset) + 1, code, desc))


class IPProtocolsViewSet(IPBaseChooserListViewSet):

    def __init__(self, **kwargs):
        IPBaseChooserListViewSet.__init__(self, data=IPTABLES_PROTOCOLS,
                                          resource_name='protocols', **kwargs)


class IPProtocolsAdvViewSet(IPBaseChooserListViewSet):

    def __init__(self, **kwargs):
        IPBaseChooserListViewSet.__init__(self, data=IPTABLES_PROTOCOLS_ADV,
                                          resource_name='protocols-adv', **kwargs)


class IPTablesViewSet(IPBaseChooserListViewSet):

    def __init__(self, **kwargs):
        IPBaseChooserListViewSet.__init__(self, data=IPTABLES_TABLES,
                                          resource_name='tables', **kwargs)


class IPTablesAdvViewSet(IPBaseChooserListViewSet):

    def __init__(self, **kwargs):
        IPBaseChooserListViewSet.__init__(self, data=IPTABLES_TABLES_ADV,
                                          resource_name='tables-adv', **kwargs)


class IPChainsViewSet(IPBaseChooserListViewSet):

    def __init__(self, **kwargs):
        IPBaseChooserListViewSet.__init__(self, data=IPTABLES_CHAINS,
                                          resource_name='chains', **kwargs)


class IPMatchExtensionsViewSet(IPBaseChooserListViewSet):

    def __init__(self, **kwargs):
        IPBaseChooserListViewSet.__init__(self, data=IPTABLES_MATCH_EXTENSIONS,
                                          resource_name='match-extensions', **kwargs)


class IPMatchExtensionsAdvViewSet(IPBaseChooserListViewSet):

    def __init__(self, **kwargs):
        IPBaseChooserListViewSet.__init__(self, data=IPTABLES_MATCH_EXTENSIONS_ADV,
                                          resource_name='match-extensions-adv', **kwargs)


# ---- End API code ---------------#

