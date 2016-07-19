import re
import os
import shlex
import subprocess

IPV4_REGEX = re.compile('^(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$')

class VNXArrayException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class VNXArray:
    """
    Provide commonly used commands as methods.
    """
    def __init__(self, hostname, user='', password='', scope=0, security_file='',  NAVICLI_PATH='/opt/Navisphere/bin/'):
        """
        Set environmental variables which will be used to run SYMCLI commands.
        """
        os.environ['PATH'] += os.pathsep + NAVICLI_PATH
        self.hostname = hostname
        self.user = user
        self.password = password
        self.scope = scope
        self.security_file = security_file

    def __repr__(self):
        """
        Return a representation string
        """
        return "<%s - %s>" % (self.__class__.__name__, self.hostname)


    def command(self, cmd):
        """
        Runs given command against VNX Array
        """
        if self.user and self.password:
            command = 'naviseccli -h {} -User {} -Password {} -Scope {} {}'.format(
                self.hostname, self.user, self.password, self.scope, cmd)
        else:
            command = 'naviseccli -h {} {}'.format(self.hostname, cmd)
        try:
            print command
            output = subprocess.check_output(shlex.split(command), stderr=subprocess.STDOUT)
            return output
        except subprocess.CalledProcessError, e:
            raise VNXArrayException("Command '%s' failed to execute successfully. Exception: %s, Output:\n %s" % (cmd, e, e.output))


    def local_command(self, cmd):
        """
        Runs given command locally (no connection to VNX is required). Mostly used for archivedump command
        """
        command = 'naviseccli {}'.format(cmd)
        try:
            output = subprocess.check_output(shlex.split(command), stderr=subprocess.STDOUT)
            return output
        except subprocess.CalledProcessError, e:
            raise VNXArrayException("Command '%s' failed to execute successfully. Exception: %s, Output:\n %s" % (cmd, e, e.output))

    def check_connectivity(self):
        result = True
        message = ''

        try:
            self.command('')
            return {'result': result, 'message': message}
        except Exception as e:
            result = False

            if re.search('Output:\n(?P<message>(.|\n)*)', e.message):
                message = re.search('Output:\n(?P<message>(.|\n)*)', e.message).groupdict()['message']
            else:
                message = e.message

        return {'result': result, 'message': message.strip()}

    def get_agent(self):
        cmd = 'getagent  -model -rev -serial -spid'
        output = self.command(cmd)

        agent_regex_str = [
            'Model:\s+(?P<model>.*)\n',
            'Revision:\s+(?P<revision>.*)\n',
            'Serial No:\s+(?P<serial_no>.*)\n',
            'SP Identifier:\s+(?P<sp_identifier>.*)\n',
        ]
        agent_regex = re.compile(''.join(agent_regex_str))

        if agent_regex.search(output):
            return agent_regex.search(output).groupdict()
        else:
            raise VNXArrayException('Unable to getagent details')


    def get_array_name(self):
        """
        Run arrayname naviseccli command, extract name and return as dictionary

        Returns:
            {'array_name': 'DC-COMPANY-HR-1'}

        Raises:
            VNXArrayException: Unable to get Array Name
        """
        output = self.command('arrayname')
        array_name_regex = re.compile('Array Name:\s+(?P<array_name>[a-zA-Z0-9_-]*)\n')
        if array_name_regex.search(output):
            return array_name_regex.search(output).groupdict()['array_name']
        else:
            raise VNXArrayException('Unable to get Array Name')

    def set_array_name(self, name):

        cmd = 'arrayname {} -o'.format(name)
        self.command(cmd)


    def get_sp_details(self, sp=None):
        """
        Run networkadmin -get commands, extract SP details like SPA or SPB, name, IP Address details as dictionary

        Args:
            sp: If supplied it will return details for that specific SP, otherwise returns SP it is connected to

        Returns:
            {'subnet_mask': '255.255.255.0', 'sp_name': 'DC-COMPANY-HR-1-A', 'sp': 'A', 'ip_address': '192.168.1.1',
            'gateway_address': '192.168.1.254'}

        Raises:
            VNXArrayException: Unable to get SP details
        """
        if sp:
            if sp.upper() not in ['A', 'B']:
                raise VNXArrayException('Invalid SP Supplied (Valid choices are A or B)')
            cmd = 'networkadmin -get -sp {} -name -ipv4'.format(sp.upper())
        else:
            cmd = 'networkadmin -get -name -ipv4'

        output = self.command(cmd)

        ipv4_regex_str = '(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
        sp_regex_str = [
            'Storage Processor:\s+SP\s(?P<sp>[AB])\n',
            'Storage Processor Network Name:\s+(?P<sp_name>[a-zA-Z0-9_-]*)\n',
            '(.|\n)*',
            'Storage Processor IP Address:\s+(?P<ip_address>{})\n'.format(ipv4_regex_str),
            'Storage Processor Subnet Mask:\s+(?P<subnet_mask>{})\n'.format(ipv4_regex_str),
            'Storage Processor Gateway Address:\s+(?P<gateway_address>{})\n'.format(ipv4_regex_str)
        ]
        SP_REGEX = re.compile(''.join(sp_regex_str))


        if SP_REGEX.search(output):
            return SP_REGEX.search(output).groupdict()
        else:
            raise VNXArrayException('Unable to get SP details')

    def set_sp_name(self, sp, name):
        if sp.upper() not in ['A', 'B']:
            raise VNXArrayException('Invalid SP Supplied (Valid choices are A or B)')

        cmd = 'networkadmin -set -sp {} -name {} -o'.format(sp, name)
        self.command(cmd)

    def get_software_list(self):
        cmd = 'ndu -list'
        output = self.command(cmd)

        software_regex_str = [
            'Name of the software package:\s*(?P<package_name>.*)\n',
            'Revision of the software package:\s*-?(?P<package_version>.*)\n',
            'Commit Required:\s*-?(?P<commit_required>.*)\n',
            'Revert Possible:\s*-?(?P<revert_possible>.*)\n',
            'Active State:\s*-?(?P<active_state>.*)\n',
            'Is installation completed:\s*-?(?P<installed>.*)\n',
            'Is this System Software:\s*-?(?P<system_software>.*)\n',
        ]

        software_regex = re.compile(''.join(software_regex_str))

        software_list = list()
        for i in software_regex.finditer(output):
            software_list.append(i.groupdict())
        return software_list



    def install_enablers(self, path_list, delay=300):
        cmd = 'ndu -install {} -force -delay {}'.format(' '.join(path_list), delay)
        output = self.command(cmd)
        print output


    def uninstall_enablers(self, name_list, delay=300):
        cmd = 'ndu -messner -uninstall {} -o -delay {}'.format(' '.join(name_list), delay)
        print cmd
        output = self.command(cmd)
        print output


    def get_software_status(self):
        cmd = 'ndu -status'
        output = self.command(cmd)
        status_regex_str = [
            'Is Completed:\s*-?(?P<is_completed>.*)\n',
            'Status:\s*-?(?P<status>.*)\n',
            'Operation:\s*-?(?P<operation>.*)\n',
        ]
        status_regex = re.compile(''.join(status_regex_str))

        if status_regex.search(output):
            return status_regex.search(output).groupdict()
        else:
            raise VNXArrayException('Unable to get software (ndu) status')


    def get_luns(self):
        output = self.command('getlun -uid -name -capacity -default -owner -rg -type -ismetalun -isthinlun -ispoollun')
        #output = self.command('getlun')
        lun_regex_str = [
            'LOGICAL UNIT NUMBER\s*(?P<lun_id>\d+)\n',
            'UID:\s*?(?P<lun_wwn>.*)\n',
            'Name\s*?(?P<lun_name>.*)\n',
            'LUN Capacity\(Megabytes\):\s*(?P<lun_capacity_mb>\d+)\n',
            'LUN Capacity\(Blocks\):\s*(?P<lun_capacity_blocks>\d+)\n',
            'Default Owner:\s*?(?P<default_owner>.*)\n',
            'Current owner:\s*?(?P<current_owner>.*)\n',
            'RAIDGroup ID:\s*(?P<raid_group_id>.*)\n',
            'RAID Type:\s*(?P<raid_group_type>.*)\n',
            'Is Meta LUN:\s*(?P<is_meta_lun>.*)\n',
            'Is Thin LUN:\s*(?P<is_thin_lun>.*)\n',
            'Is Pool LUN:\s*(?P<is_pool_lun>.*)\n',
        ]
        lun_regex = re.compile(''.join(lun_regex_str))
        #print "%r" % ''.join(lun_regex_str)
        luns = []
        for i in lun_regex.finditer(output):
            luns.append(i.groupdict())
        return luns


    def get_sp_port_details(self):
        output = self.command("port -list -sp -all")

        sp_regex_str = [
            'SP Name:\s*-?(?P<sp_name>.*)\n',
            'SP Port ID:\s*-?(?P<sp_port_id>.*)\n',
            'SP UID:\s*-?(?P<sp_uid>.*)\n',
            'Link Status:\s*-?(?P<link_status>.*)\n',
            'Port Status:\s*-?(?P<port_status>.*)\n',
            'Switch Present:\s*-?(?P<switch_present>.*)\n',
            '(Switch UID:\s*-?(?P<switch_uid>.*)\n)?',
            '(SP Source ID:\s*-?(?P<sp_source_id>.*)\n)?',
            'ALPA Value:\s*-?(?P<alpa_value>.*)\n',
            'Speed Value :\s*-?(?P<speed_value>.*)\n',
        ]
        sp_regex = re.compile(''.join(sp_regex_str))

        ports = []
        for i in sp_regex.finditer(output):
            ports.append(i.groupdict())

        if not ports:
            raise VNXArrayException('Unable to get port details')
        else:
            return ports


    def get_storagegroups(self):
        output = self.command("storagegroup -list")
        sg_regex_str = [
            'Storage Group Name:\s*(?P<sg_name>.*)\n',
            'Storage Group UID:\s*(?P<sg_uid>.*)\n',
        ]
        sg_regex = re.compile(''.join(sg_regex_str))

        storage_groups = []
        for i in sg_regex.finditer(output):
            storage_groups.append(i.groupdict())
        return storage_groups



    def storagepool_list(self):
        output = self.command('storagepool -list -availableCap -consumedCap')
        output = self.command('storagepool -list')
        print output

    def get_disk_details(self):
        output = self.command('getdisk -vendor -product -lun -type -state -hs -serial -tla -rg')

        disk_regex_str = [
            '(Bus (?P<bus>\d+) Enclosure (?P<enclosure>\d+)  Disk (?P<disk>\d+)\n)?',
            '(Vendor Id:\s*(?P<vendor_id>.*)\n)?',
            '(Product Id:\s*(?P<product_id>.*)\n)?',
            '(Lun:\s*(?P<lun>.*)\n)?',
            '(Type:\s*(?P<type>.*)\n)?',
            'State:\s*(?P<state>.*)\n',
            '(Hot Spare:\s*(?P<hot_spare>.*)\n)?',
            '(Serial Number:\s*(?P<serial_number>.*)\n)?',
            '(Clariion TLA Part Number:\s*?(?P<tla>.*)\n)?',
            '(Raid Group ID:\s*?(?P<raid_group_id>.*)\n)?',
        ]

        disk_regex = re.compile(''.join(disk_regex_str))

        disks = []
        for i in disk_regex.finditer(output):
            disks.append(i.groupdict())

        if not disks:
            raise VNXArrayException('Unable to get disk details')
        else:
            return disks

    def get_ntp(self):
        output = self.command('ntp -list -all')

        ntp_regex_str = [
            'start:\s*(?P<start>.*)\n',
            'interval:\s*(?P<interval>.*)\n',
            'address:\s*(?P<address>.*)\n',
        ]
        ntp_regex = re.compile(''.join(ntp_regex_str))

        if ntp_regex.search(output):
            return ntp_regex.search(output).groupdict()
        else:
            raise VNXArrayException('Unable to get NTP Details')





"""
^Radha Kalyana(\s|-){1,4}Episode(\s|-){1,4}(?P<episode_number>\d+)(\s|-){1,4}(?P<month>[-\w]+)(\s|-){1,4}(?P<day>\d+)(\s|,|'){1,3}(?P<year>\d+)$
"""