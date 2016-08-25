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
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.db import models
from proj.models import BaseModel
from apps.rules.models import AbstractMachineSubset, AbstractMachineSet, Bundle

IPTABLES_TRANSPORT_VERSION = (
    (1, 'ipv4'),
    (2, 'ipv6'),
    (3, 'both'),
)

IPTABLES_PROTOCOLS = (
    ('all', _('All')),
    ('tcp', _('tcp')),
    ('udp', _('udp')),
    ('icmp', _('icmp')),
)

IPTABLES_PROTOCOLS_ADV = (
    ('all', _('all')),
    ('tcp', _('tcp')),
    ('udp', _('udp')),
    ('icmp', _('icmp')),
    ('udplite', _('udplite')),
    ('esp', _('esp')),
    ('ah', _('ah')),
    ('sctp', _('sctp')),
)

IPTABLES_TABLES = (
    ('filter', _('Filter')),
    ('nat', _('Nat')),
)

IPTABLES_TABLES_ADV = (
    ('filter', _('Filter')),
    ('nat', _('Nat')),
    ('mangle', _('Mangle')),
    ('raw', _('Raw')),
    ('security', _('Security')),
    ('all', _('All')),
)

IPTABLES_CHAINS = (
    ('input', _('Input')),
    ('output', _('Output')),
    ('forward', _('Forward')),
    ('prerouting', _('Pre-Routing')),
    ('postrouting', _('Post-Routing')),
)

# TODO: Fill out match extension list and advanced match extension list
IPTABLES_MATCH_EXTENSIONS = (
    ('state', _('State')),
)

IPTABLES_MATCH_EXTENSIONS_ADV = (
    ('state', _('State')),
)

# # Add the bundle options to the apps.rules.Bundle object and
# # auto create the bundle options database record if it does not exist
# Bundle.options = property(lambda b: IPTablesBundleOptions.objects.get_or_create(bundle=b)[0])
#
#
# class IPTablesBundleOptions(BaseModel):
#
#     bundle = models.OneToOneField(Bundle)
#
#     log_output_filter_tbl = models.BooleanField(_('Log output chain on Filter Table.'), default=True)
#     log_output_nat_tbl = models.BooleanField(_('Log output chain on NAT Table.'), default=False)
#     log_output_mangle_tbl = models.BooleanField(_('Log output chain on Mangle Table.'), default=False)
#     log_output_raw_tbl = models.BooleanField(_('Log output chain on Raw Table.'), default=False)
#     log_output_security_tbl = models.BooleanField(_('Log output chain on Security Table.'), default=False)
#
#     class Meta:
#         db_table = 'iptables_bundle_options'


class IPTablesMachineSubset(AbstractMachineSubset):

    platform = models.CharField(_('Firewall Platform'), max_length=30, default='iptables')

    class Meta:
        db_table = 'iptables_machine_subset'
        ordering = ['slot', 'sort_id']


class IPTablesMachineSet(AbstractMachineSet):

    machine_subset = models.ForeignKey(IPTablesMachineSubset, related_name='machine_sets')
    enabled = models.BooleanField(_('Enabled'), default=False)
    panic = models.BooleanField(_('Panic'), default=False)

    class Meta:
        db_table = 'iptables_machine_set'
        

# FYI, IPTablesChain is not the same thing as an iptables table chain (IE: prerouting).
class IPTablesChain (BaseModel):

    machine_subset = models.ForeignKey(IPTablesMachineSubset, on_delete=models.CASCADE, related_name="chains")
    name = models.CharField(_('IPTables Table'), max_length=15, choices=IPTABLES_TABLES)

    class Meta:
        db_table = 'iptables_chain'


class IPTablesRing (BaseModel):

    chain = models.ForeignKey(IPTablesChain, on_delete=models.CASCADE, related_name="rings")
    name = models.CharField(_('IPTables Table Chain'), max_length=15, choices=IPTABLES_CHAINS)
    version = models.CharField(_('Transport Version'), max_length=4, choices=IPTABLES_TRANSPORT_VERSION)

    class Meta:
        db_table = 'iptables_ring'


class IPTablesRule (BaseModel):

    ring = models.ForeignKey(IPTablesRing, on_delete=models.CASCADE, related_name="rules")
    enabled = models.BooleanField(_('Enabled'))
    sort_id = models.SmallIntegerField(_('Sort ID'), null=True, blank=True)
    descr = models.CharField(_('Description'), max_length=500, default='', null=True, blank=True)
    
    #interface in
    ifacein_name = models.CharField(_('Name'), max_length=25, null=True, blank=True)
    ifacein_invert = models.BooleanField(_('Invert'), default=False)
    
    #interface out
    ifaceout_name = models.CharField(_('Name'), max_length=25, null=True, blank=True)
    ifaceout_invert = models.BooleanField(_('Invert'), default=False) 
    
    #IP protocol
    ip_protocol_name = models.CharField(_('Name'), max_length=25, choices=IPTABLES_PROTOCOLS, null=True, blank=True)
    ip_protocol_invert = models.BooleanField(_('Invert'), default=False)
      
    #source  
    source_address = models.CharField(_('Address'), max_length=255, null=True, blank=True)
    # Mask value can be 1 -> 31 for ipv4 and 1 -> 127 for ipv6
    source_mask = models.SmallIntegerField(_('Mask'), null=True, blank=True)
    source_invert = models.BooleanField(_('Invert'), default=False)
    
    #destination
    dest_address = models.CharField(_('Address'), max_length=255, null=True, blank=True)
    # Mask value can be 1 -> 31 for ipv4 and 1 -> 127 for ipv6
    dest_mask = models.SmallIntegerField(_('Mask'), null=True, blank=True)
    dest_invert = models.BooleanField(_('Invert'), default=False) 
    
    #fragment
    fragment = models.BooleanField(_('Fragment'), default=False)
    fragment_invert = models.BooleanField(_('Invert'), default=False)               
    
    class Meta:
        db_table = 'iptables_rule'
        ordering = ['sort_id']
        
    @classmethod    
    def edit(cls, POST_values, rule_id):
      
        txt_cleaner = forms.CharField()
        ip_cleaner = forms.GenericIPAddressField()
        
        # get the posted data for the Rule edit
        txt_cleaner.required = True
        transport = txt_cleaner.clean( POST_values['transport']) 
        
        txt_cleaner.required = False
        enabled = txt_cleaner.clean( POST_values['enabled'] )  
        description = txt_cleaner.clean( POST_values['description'] )  
        protocol = txt_cleaner.clean( POST_values['protocol'] )  
        table = txt_cleaner.clean( POST_values['table'] )  
        chain = txt_cleaner.clean( POST_values['chain'] )  
        ifacein = txt_cleaner.clean( POST_values['ifacein'] ) 
        ifaceout = txt_cleaner.clean( POST_values['ifaceout'] ) 
        source_address = txt_cleaner.clean( POST_values['source-address'] )  
        source_mask = txt_cleaner.clean( POST_values['source-mask'] )  
        dest_address = txt_cleaner.clean( POST_values['dest-address'] )  
        dest_mask = txt_cleaner.clean( POST_values['dest-mask'] )
        
        if source_mask in ( '','None')  :
            source_mask = None
        else:
            source_mask = int(source_mask)    
            
        if dest_mask in ( '', 'None'):
            dest_mask = None
        else:
            dest_mask = int(dest_mask)            
            
        
        # retrieve the rule from the database
        edited_rule = IPTablesRule.objects.get(id=rule_id)
         
        # assign posted values to the rule 
        edited_rule.enabled = True if( enabled == 'Enabled' ) else False #cheezy syntax but works
        edited_rule.description = description
        edited_rule.transport = transport
        edited_rule.ip_protocol_name = protocol  
        edited_rule.ifacein_name = ifacein
        edited_rule.ifaceout_name = ifaceout  
        edited_rule.source_address = source_address  
        edited_rule.source_mask = source_mask
        edited_rule.dest_address = dest_address 
        edited_rule.dest_mask = dest_mask
        
        #reset 'invert' booleans
        edited_rule.ifacein_invert = False
        edited_rule.ifaceout_invert = False
        edited_rule.ip_protocol_invert = False
        edited_rule.source_invert = False
        edited_rule.dest_invert = False
            
        #set the 'inverts' that are checked on the rule edit page
        if  POST_values.get('ifacein_invert'):
            edited_rule.ifacein_invert = True
        if  POST_values.get('ifaceout_invert'):
            edited_rule.ifaceout_invert = True 
        if  POST_values.get('protocol_invert'):
            edited_rule.ip_protocol_invert = True
        if  POST_values.get('source_invert'):
            edited_rule.source_invert = True
        if  POST_values.get('dest_invert'):
            edited_rule.dest_invert = True                                                   
            
        # save the new values for the rule being edited    
        edited_rule.save()  
      
      
        return        


class IPTablesMatch (BaseModel):
  
  
    #~ match_fields = {"tcp": ["Source Port", "Destination Port", "TCP Flags", "Syn", "TCP Option"], 
                        #~ "state":["state"], 
                        #~ "conntrack": ["ctstate", "ctproto", "ctorigsrc", "ctorigdst", "ctorigsrcport", "ctoringdstport", "ctrepldstport", "cstatus", "ctexpire", "ctdir"]}    
  
    match_fields = {
                    "addrtype":[{"name":"src-type","invertible":"True"}, {"name":"dst-type","invertible":"True"}, 
                                {"name":"limit-iface-in","invertible":"False"}, {"name":"limit-iface-out","invertible":"False"}],
                    "ah-ipv6":[{"name":"ahspi","invertible":"True"}, {"name":"ahlen","invertible":"True"}, 
                               {"name":"ahres","invertible":"False"}],
                    "ah-ipv4":[{"name":"ahspi","invertible":"True"}],
                    "bpf":[{"name":"bytecode","invertible":"False"}],
                    "cluster":[{"name":"cluster-total-nodes","invertible":"False"}, {"name":"cluster-local-node","invertible":"True"},
                               {"name":"cluster-local-nodemask","invertible":"True"}, {"name":"cluster-hash-seed","invertible":"False"}],
                    "comment":[{"name":"comment","invertible":"False"}],
                    "connbytes":[{"name":"connbytes","invertible":"True"}, {"name":"connbytes-dir","invertible":"False"}, 
                                 {"name":"connbytes-mode","invertible":"False"}],
                    "connlabel":[{"name":"label","invertible":"True"}, {"name":"set", "invertible":"False"}],
                    "connlimit":[{"name":"connlimit-upto","invertible":"False"}, {"name":"connlimit-above", "invertible":"False"},
                                 {"name":"connlimit-mask","invertible":"False"}, {"name":"connlimit-saddr", "invertible":"False"},
                                 {"name":"connlimit-daddr","invertible":"False"} ],
                    "connmark":[{"name":"mark","invertible":"True"}],
                    "conntrack":[{"name":"ctstate", "invertible":"True"}, {"name":"ctproto", "invertible":"True"}, 
                                 {"name":"ctorigsrc", "invertible":"True"}, {"name":"ctorigdst", "invertible":"True"}, 
                                 {"name":"ctorigsrcport", "invertible":"True"}, {"name":"ctoringdstport", "invertible":"True"}, 
                                 {"name":"ctrepldstport", "invertible":"True"}, {"name":"cstatus", "invertible":"True"}, 
                                 {"name":"ctexpire", "invertible":"True"}, {"name":"ctdir", "invertible":"True"}],
                    "cpu":[{"name":"cpu","invertible":"True"}],
                    "dccp":[{"name":"source-port","invertible":"True"}, {"name":"destination-port","invertible":"True"}, 
                            {"name":"dccp-types","invertible":"True"}, {"name":"dccp-option","invertible":"True"}],
                    "devgroup":[{"name":"src-group","invertible":"True"}, {"name":"dst-group", "invertible":"True"}],
                    "dscp":[{"name":"dscp","invertible":"True"}, {"name":"dscp-class", "invertible":"True"}],
                    "dst":[{"name":"dst-len","invertible":"True"}, {"name":"dst-opts", "invertible":"False"}],
                    "ecn":[{"name":"ecn-tcp-cwr","invertible":"True"}, {"name":"ecn-tcp-ece","invertible":"True"}, 
                           {"name":"ecn-ip-ect","invertible":"True"}],
                    "esp":[{"name":"espspi","invertible":"True"}],
                    "eui64":[],
                    "frag":[{"name":"fragid","invertible":"True"}, {"name":"fraglen","invertible":"True"},
                            {"name":"fragres", "invertible":"False"}, {"name":"fragfirst","invertible":"False"},
                            {"name":"fragmore", "invertible":"False"}, {"name":"fraglast", "invertible":"False"}],
                    "hashlimit":[{"name":"hashlimit-upto", "invertible":"False"}, {"name":"hashlimit-above", "invertible":"False"}, 
                                 {"name":"hashlimit-burst", "invertible":"False"}, {"name":"hashlimit-mode", "invertible":"False"}, 
                                 {"name":"hashlimit-srcmask", "invertible":"False"}, {"name":"hashlimit-dstmask", "invertible":"False"}, 
                                 {"name":"hashlimit-name", "invertible":"False"}, {"name":"hashlimit-htable-size", "invertible":"False"}, 
                                 {"name":"hashlimit-htable-max", "invertible":"False"}, {"name":"hashlimit-htable-expire", "invertible":"False"}, 
                                 {"name":"hashlimit-htable-gcinterval", "invertible":"False"}],
                    "hbh":[{"name":"hbh-len","invertible":"True"}, {"name":"hbh-opts","invertible":"False"}],
                    "helper":[{"name":"helper","invertible":"True"}],
                    "hl":[{"name":"hl-eq","invertible":"True"}, {"name":"hl-lt","invertible":"False"},
                          {"name":"hl-gt","invertible":"False"}],
                    "icmp":[{"name":"icmp-type","invertible":"True"}],
                    "icmp6":[{"name":"icmpv6-type","invertible":"True"}],
                    "iprange":[{"name":"src-range","invertible":"True"}, {"name":"dst-range", "invertible":"True"}],
                    "ipv6header":[{"name":"soft", "invertible":"False"}, {"name":"header", "invertible":"True"}, 
                                  {"name":"hop", "invertible":"False"}, {"name":"dst", "invertible":"False"}, 
                                  {"name":"route", "invertible":"False"}, {"name":"frag", "invertible":"False"}, 
                                  {"name":"auth", "invertible":"False"}, {"name":"esp", "invertible":"False"}, 
                                  {"name":"none", "invertible":"False"}, {"name":"proto", "invertible":"False"}],
                    "ipvs":[{"name":"ipvs","invertible":"True"}, {"name":"vproto", "invertible":"True"},
                            {"name":"vaddr","invertible":"True"}, {"name":"vport", "invertible":"True"},
                            {"name":"vdir","invertible":"False"}, {"name":"vmethod", "invertible":"True"},                                 
                            {"name":"vportctl","invertible":"True"} ],
                    "length":[{"name":"length","invertible":"True"}],
                    "limit":[{"name":"limit","invertible":"False"}, {"name":"limit-burst", "invertible":"False"}],
                    "mac":[{"name":"mac-source","invertible":"True"}],
                    "mark":[{"name":"mark","invertible":"True"}],
                    "mh":[{"name":"mh-type","invertible":"True"}],
                    "multiport":[{"name":"source-ports","invertible":"True"}, {"name":"destination-ports","invertible":"True"},
                                 {"name":"ports","invertible":"True"}],
                    "nfacct":[{"name":"nfacct-name","invertible":"False"}],
                    "osf":[{"name":"genre","invertible":"True"}, {"name":"ttl","invertible":"False"}, 
                           {"name":"log","invertible":"False"}],
                    "owner":[{"name":"uid-owner","invertible":"True"}, {"name":"uid-owner", "invertible":"True"},
                             {"name":"gid-owner","invertible":"True"}, {"name":"gid-owner", "invertible":"True"},
                             {"name":"socket-exists","invertible":"True"}],
                    "physdev":[{"name":"physdev-in","invertible":"True"}, {"name":"physdev-out", "invertible":"True"},
                               {"name":"physdev-is-in","invertible":"True"}, {"name":"physdev-is-out", "invertible":"True"},
                               {"name":"physdev-is-bridged","invertible":"True"}],
                    "pkttype":[{"name":"pkt-type","invertible":"True"}],
                    "policy": [{"name":"dir", "invertible":"False"}, {"name":"pol", "invertible":"False"}, 
                               {"name":"strict", "invertible":"False"}, {"name":"reqid", "invertible":"True"}, 
                               {"name":"spi", "invertible":"True"}, {"name":"proto", "invertible":"True"}, 
                               {"name":"mode", "invertible":"True"}, {"name":"tunnel-src", "invertible":"True"}, 
                               {"name":"tunnel-dst", "invertible":"True"}, {"name":"next", "invertible":"False"}],
                    "quota":[{"name":"quota","invertible":"True"}],
                    "raatest":[{"name":"raatest-delta", "invertible":"False"}, {"name":"raatest-lt", "invertible":"True"}, 
                               {"name":"raatest-gt", "invertible":"True"}, {"name":"raatest-eq", "invertible":"True"}, 
                               {"name":"raatest", "invertible":"False"}, {"name":"raatest1", "invertible":"False"}, 
                               {"name":"raatest2", "invertible":"False"}, {"name":"raatest-bps", "invertible":"False"}, 
                               {"name":"raatest-pps", "invertible":"False"}, {"name":"raatest-bps1", "invertible":"False"},
                               {"name":"raatest-bps2", "invertible":"False"}, {"name":"raatest-pps1", "invertible":"False"},
                               {"name":"raatest-pps2", "invertible":"False"}],
                    "realm":[{"name":"realm","invertible":"True"}],
                    "recent":[{"name":"name", "invertible":"False"}, {"name":"set", "invertible":"True"}, 
                              {"name":"rsource", "invertible":"False"}, {"name":"rdest", "invertible":"False"}, 
                              {"name":"mask", "invertible":"False"}, {"name":"rcheck", "invertible":"True"}, 
                              {"name":"update", "invertible":"True"}, {"name":"remove", "invertible":"True"},
                              {"name":"seconds", "invertible":"False"}, {"name":"reap", "invertible":"False"},
                              {"name":"hitcount", "invertible":"False"}, {"name":"rttl", "invertible":"False"}],
                    "rpfilter":[{"name":"loose","invertible":"False"}, {"name":"validmark","invertible":"False"}, 
                                {"name":"accept-local","invertible":"False"}, {"name":"invert","invertible":"False"}],
                    "rt":[{"name":"rt-type","invertible":"True"}, {"name":"rt-segsleft","invertible":"True"},
                          {"name":"rt-len", "invertible":"True"}, {"name":"rt-0-res","invertible":"False"},
                          {"name":"rt-0-addrs", "invertible":"False"}, {"name":"rt-0-not-strict", "invertible":"False"}],
                    "sctp":[{"name":"source-port","invertible":"True"}, {"name":"destination-port","invertible":"True"}, 
                            {"name":"chunk-types","invertible":"True"}],
                    "set":[{"name":"match-set", "invertible":"True"}, {"name":"return-nomatch", "invertible":"False"}, 
                           {"name":"update-counters", "invertible":"True"}, {"name":"update-subcounters", "invertible":"True"}, 
                           {"name":"packets-eq", "invertible":"True"}, {"name":"packets-lt", "invertible":"False"}, 
                           {"name":"packets-gt", "invertible":"False"}, {"name":"bytes-eq", "invertible":"True"}, 
                           {"name":"bytes-lt", "invertible":"False"}, {"name":"bytes-gt", "invertible":"False"}],
                    "socket":[{"name":"transplant","invertible":"False"}, {"name":"nowildcard", "invertible":"False"}],
                    "state":[{"name":"state", "invertible":"True"}],
                    "statistic":[{"name":"mode","invertible":"False"}, {"name":"probability","invertible":"True"},
                           {"name":"every","invertible":"True"}, {"name":"packet","invertible":"False"}],
                    "string":[{"name":"algo","invertible":"False"}, {"name":"from", "invertible":"False"},
                              {"name":"to","invertible":"False"}, {"name":"string", "invertible":"True"},
                              {"name":"hex-string","invertible":"True"}],
                    "tcp":[{"name":"source-port","invertible":"True"}, {"name":"destination-port","invertible":"True"},
                           {"name":"tcp-flags", "invertible":"True"}, {"name":"syn","invertible":"True"},
                           {"name":"tcp-option", "invertible":"True"}],
                    "tcpmss":[{"name":"mss","invertible":"True"}],
                    "time":[{"name":"datestart", "invertible":"False"}, {"name":"datestop", "invertible":"False"},
                            {"name":"timestart", "invertible":"False"}, {"name":"timestop", "invertible":"False"},
                            {"name":"monthdays", "invertible":"True"}, {"name":"weekdays", "invertible":"True"},
                            {"name":"contiguous", "invertible":"False"}, {"name":"kerneltz", "invertible":"False"}],
                    "tos":[{"name":"tos","invertible":"True"}, {"name":"tos", "invertible":"True"}],
                    "ttl":[{"name":"ttl-eq","invertible":"True"}, {"name":"ttl-gt","invertible":"False"}, 
                            {"name":"ttl-lt","invertible":"False"}],
                    "u32":[{"name":"u32", "invertible":"True"}],
                    "udp":[{"name":"source-port","invertible":"True"}, {"name":"destination-port","invertible":"True"}],
                    "unclean":[{"name":"assert","invertible":"False"}],
                     
                    }   # end of match_fields structure             
    
  

    rule = models.ForeignKey(IPTablesRule, on_delete=models.CASCADE, related_name='matches')
    name = models.CharField(_('Name'), null=True, blank=True, max_length=50, choices=IPTABLES_MATCH_EXTENSIONS)

    class Meta:
        db_table = 'iptables_match'
        
    @classmethod     
    def save_matches(cls, POST_values, form_prefixes_and_ids, rule_id):
        txt_cleaner = forms.CharField()   # use this to clean incoming form data
        edited_rule = IPTablesRule.objects.get(id=rule_id)
        
        # get identifiers for all new, old and delete matches
        all_new_matches = []
        all_old_matches = []
        all_delete_matches = []
        
        #get old and new matches
        for match_type in cls.match_fields:
            for key in POST_values:
                if 'newindex_' + match_type.lower() in key:
                    all_new_matches.append(key)
                     
                elif 'oldindex_' + match_type.lower() in key:
                     all_old_matches.append(key)   
        
        #get delete matches             
        for key in POST_values:              
            if 'delete_' in key:
                all_delete_matches.append(key)                          
                     
        for key in all_delete_matches:
            delete_match_id = POST_values[key].strip()
            match_to_delete = IPTablesMatch.objects.get(id=delete_match_id)
            match_to_delete.delete()
                 
        # check that there is valid match data to be saved for each new match
        # save it if there is
        for match in all_new_matches:
            last_underscore = match.rfind('_')
            first_underscore = match.find('_')+1
            match_type = match[first_underscore:last_underscore]
            match_id = match[last_underscore+1:]
            empty_post = True
            
            for key in POST_values:
                if match_id in key and 'new' in key:
                    is_it_null = POST_values[key].strip()
                    if is_it_null != '':
                        empty_post = False
                        
            if not empty_post:
              # post has some data so save the match
                this_match = IPTablesMatch(rule=edited_rule, name=str(match_type) )
                this_match.save()                    
                for key in POST_values:
                    # create a match option for each field received                        
                    if match_id in key and 'newindex' not in key and 'old' not in key and 'oldindex' not in key and 'new' in key and '_cb' not in key:
                        option_name = key[:key.rfind('_')]
                        option_value = POST_values[key]
                        #print( "option name: ", option_name, " option_value: ", option_value, " key: " , key)
                        
                        #set the 'invert' flag for this option
                        if POST_values.get(key+'_cb', 'not here') == 'not here':
                            is_inverted = False
                        else:
                            is_inverted = True
                            
                        #determine if this match option is invertible
                        invertible = None
                        for option in cls.match_fields[match_type]:
                            if option['name'] == option_name:
                                invertible = option['invertible']
                                if invertible == "True": invertible = True
                                if invertible == "False": invertible = False
                        
                        this_match_option = IPTablesMatchOptions(match_name=this_match, option=option_name, value=option_value, invertible=invertible, invert=is_inverted, sort_id=1)
                        this_match_option.save()
                        
            else:
                # the data for this match is all null
                pass
                
        #Save the form match option values of the pre-existing matches        
        #Go through all the match codes stored in the session. Use the code to find corresonding
        #match option names and values.  Update the match_option values.        
        for prefix in form_prefixes_and_ids :
          
            for key in POST_values:
              
                if prefix[0] in key :
                  
                    #The field name occurs in the key at a fixed offset from the left side  
                    field_name = key[16:]
                    
                    #Update the match option value in the database. Make sure this key is not a check box. 
                    if field_name != '' and '_cb' not in field_name :
                        
                        try:
                            this_match_option = IPTablesMatchOptions.objects.get(match_name=prefix[1], option=field_name)
                            
                            # this shouldn't be required as blank=True in the model but it throws an exception anyway
                            txt_cleaner.required = False
                            this_match_option.value = txt_cleaner.clean( POST_values[key] ) 

                            #set the 'invert' flag for this option
                            if POST_values.get(key+'_cb', 'not here') == 'not here':
                                this_match_option.invert = False
                            else:
                                this_match_option.invert = True                                
                            
                            this_match_option.save()
                        except Exception as e:
                            #print("error: ", e)
                            pass 
        return    


class IPTablesMatchOptions (BaseModel):

    match_name = models.ForeignKey(IPTablesMatch, on_delete=models.CASCADE, related_name='options')
    option = models.CharField(_('Option'), null=True, blank=True, max_length=50)
    value = models.CharField(_('Value'), null=True, blank=True, max_length=1000)
    invertible = models.BooleanField(_('Invertible'), default=False) 
    invert = models.BooleanField(_('Invert'), default=False)
    sort_id = models.SmallIntegerField(_('Sort ID'), null=True, blank=True)

    class Meta:
        db_table = 'iptables_match_options'
        ordering = ['sort_id']
        
        
class IPTablesJump (BaseModel):
  
    jump_fields = {
                   "audit":["type"],
                   "checksum":["checksum-fill"],
                   "classify":["set-class"],
                   "clusterip":["new","hashmode", "clustermac", "total-nodes", "local-node", "hash-init"],
                   "connmark":["set-xmark", "save-mark", "restore-mark", "and-mark", "or-mark", "xor-mark", "set-mark", "save-mark", "restore-mark"],
                   "connsecmark":["save","restore"],
                   "ct":["notrack", "helper", "ctevents", "expevents", "zone", "timeout"],
                   "dnat":["to-destination", "random", "persistant"],
                   "dnpt":["src-pfx", "dst-pfx"],
                   "dscp":["set-dscp","set-dscp-class"],
                   "ecn":["ecn-tcp-remove"],
                   "hl":["hl-set","hl-dec", "hl-inc"],
                   "hmark":["hmark-tuple", "hmark-mod", "hmark-offset", "hmark-src-prefix", "hmark-dst-prefix", "hmark-sport-mask", 
                            "hmark-dport-mask", "hmark-spi-mask", "hmark-proto-mask", "hmark-rnd"],
                   "ideltimer":["timeout", "label"],
                   "led":["led-trigger", "led-delay", "led-always-blink"],
                   "log": ["level", "prefix", "tcp-sequence", "tcp-options", "ip-options", "uid"],
                   "mark":["set-xmark", "set-mark", "and-mark", "or-mark", "xor-mark"],
                   "masquerade":["to_ports", "random"],
                   "mirror":[],
                   "netmap":["to"],
                   "nflog":["nflog-group", "nflog-prefix", "nflog-range", "nflog-threshold"],
                   "nfqueue":["queue-num", "queue-balance", "queue-bypass", "queue-cpu-fanout"],
                   "notrack":[],
                   "rateest":["rateest-name", "rateest-interval", "rateest-ewmalog"],
                   "redirect":["to-ports", "random"],
                   "reject-ipv6": ["reject-with"], 
                   "reject-ipv4": ["reject-with"],
                   "same":["to", "nodst", "random"],
                   "secmark":["selctx"],
                   "set":["add-set", "del-set", "timeout", "exit"],
                   "snat":["ro-source", "random", "persistent"],
                   "snpt":["src-pfx", "dst-pfx"],
                   "tcpmss":["set-mss", "clamp-mss-to-mptu"],
                   "tcpoptstrip":["strip-options"],
                   "tee":["gateway"],
                   "tos":["set-tos", "set-tos", "and-tos", "or-tos", "xor-tos"],
                   "tproxy":["on-port", "on-ip", "tproxy-mark"],
                   "trace":[],
                   "ttl":["ttl-set", "ttl-dec", "ttl-inc"],
                   "ulog":["ulog-nlgroup", "ulog-prefix", "ulog-cprange", "ulog-qthreshold"],
                   "drop": [],
                   "accept": [], 
                   }                
    

    rule = models.OneToOneField(IPTablesRule, related_name='jump')
    target = models.CharField(_('Target'), max_length=50)

    class Meta:
        db_table = 'iptables_jump'


class IPTablesJumpOptions (BaseModel):

    jump = models.ForeignKey(IPTablesJump, on_delete=models.CASCADE, related_name='params')
    name = models.CharField(_('Value'), null=True, blank=True, max_length=50)
    value = models.CharField(_('Value'), null=True, blank=True, max_length=255)
    
     

    class Meta:
        db_table = 'iptables_jump_options'  
    
    @classmethod    
    def save_options(cls, POST_values, rule_id):
        txt_cleaner = forms.CharField()
        
        # save the jump (and jump options) data                                
        target =  txt_cleaner.clean(POST_values['jump_target'] ) 
        
        #check to see if a jump entry already exists for this rule
        does_jump_exist = IPTablesJump.objects.filter(rule=rule_id).count()
        this_jump = None
        if does_jump_exist == 0:
            # create a jump for this rule if it doesn't exist
            new_jump = IPTablesJump(rule=rule_id, target=target)
            new_jump.save()
            this_jump = new_jump
        elif does_jump_exist == 1:
            this_jump = IPTablesJump.objects.get(rule=rule_id)
            this_jump.target = target
            this_jump.save()
            
        jump_option_delete = True  
        for key in POST_values:  
            
            if '_jump' in key:
                #jump options exist so store them but first remove existing options
                if jump_option_delete == True:
                    jump_option_delete = False #reset delete jump option flag
                    jump_options_to_delete = IPTablesJumpOptions.objects.filter(jump=this_jump)
                    for jump_option in jump_options_to_delete:
                        jump_option.delete()
                 
                txt_cleaner.required = True    
                jump_name = txt_cleaner.clean(key[:-5])
                txt_cleaner.required = False
                jump_value = txt_cleaner.clean(POST_values[key])  
                       
                this_jump_option = IPTablesJumpOptions(jump=this_jump, name=jump_name, value=jump_value)
                this_jump_option.save()
                
                #print( jump_name, "  ", jump_value)
                
        if target in ('Drop', 'Accept'):
            # these targets have no options so remove them
            jump_options_to_delete = IPTablesJumpOptions.objects.filter(jump=this_jump)
            for jump_option in jump_options_to_delete:
                jump_option.delete() 
                
        return        
        
   



#class IPTablesIFaceIn (BaseModel):

    #rule = models.OneToOneField(IPTablesRule, related_name='ifaceIn')
    #name = models.CharField(_('Name'), max_length=25)
    #invert = models.BooleanField(_('Invert'))

    #class Meta:
        #db_table = 'iptables_ifacein'


#class IPTablesIFaceOut (BaseModel):

    #rule = models.OneToOneField(IPTablesRule, related_name='ifaceOut')
    #name = models.CharField(_('Name'), max_length=25)
    #invert = models.BooleanField(_('Invert'))

    #class Meta:
        #db_table = 'iptables_ifaceout'


#class IPTablesProtocol (BaseModel):

    #rule = models.ForeignKey(IPTablesRule, related_name='protocol')
    #name = models.CharField(_('Name'), max_length=25, choices=IPTABLES_PROTOCOLS)
    #invert = models.BooleanField(_('Invert'))

    #class Meta:
        #db_table = 'iptables_protocol'


#class IPTablesSource (BaseModel):

    ## TODO: Setup Validator for address and Mask
    #rule = models.ForeignKey(IPTablesRule, related_name='source')
    #address = models.CharField(_('Address'), max_length=255)
    ## Mask value can be 1 -> 31 for ipv4 and 1 -> 127 for ipv6
    #mask = models.SmallIntegerField(_('Mask'))
    #invert = models.BooleanField(_('Invert'))

    #class Meta:
        #db_table = 'iptables_source'


#class IPTablesDestination (BaseModel):

    ## TODO: Setup Validator for address and Mask
    #rule = models.ForeignKey(IPTablesRule, related_name='destination')
    #address = models.CharField(_('Address'), max_length=255)
    ## Mask value can be 1 -> 31 for ipv4 and 1 -> 127 for ipv6
    #mask = models.SmallIntegerField(_('Mask'))
    #invert = models.BooleanField(_('Invert'))

    #class Meta:
        #db_table = 'iptables_destination'


## IPTablesFragment only available for ipv4 rules
#class IPTablesFragment (BaseModel):

    #rule = models.ForeignKey(IPTablesRule, related_name='fragment')
    #fragment = models.BooleanField(_('Fragment'), default=False)
    #invert = models.BooleanField(_('Invert'), default=False)

    #class Meta:
        #db_table = 'iptables_fragment'


#class IPTablesMatch (BaseModel):

    #rule = models.ForeignKey(IPTablesRule, related_name='matches')
    #name = models.CharField(_('Value'), max_length=50, choices=IPTABLES_MATCH_EXTENSIONS)

    #class Meta:
        #db_table = 'iptables_match'


#class IPTablesMatchOptions (BaseModel):

    #matchName = models.ForeignKey(IPTablesMatch, related_name='options')
    #option = models.CharField(_('Option'), max_length=50)
    #value = models.CharField(_('Value'), max_length=1000)
    #invert = models.BooleanField(_('Invert'))
    #sortId = models.SmallIntegerField(_('Sort ID'))

    #class Meta:
        #db_table = 'iptables_match_options'
        #ordering = ['sortId']



