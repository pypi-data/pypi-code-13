"""
mbed SDK
Copyright (c) 2011-2015 ARM Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import subprocess
import plistlib
import platform


from lstools_darwin import MbedLsToolsDarwin

class MbedLsToolsElCapitan(MbedLsToolsDarwin):
    """ MbedLsToolsElCapitan supports mbed-enabled platforms detection on OSX El Capitan
    """

    def get_mbed_volumes(self):
        ''' returns a map {volume_id: {serial:, vendor_id:, product_id:, tty:}'''

        # to find all the possible mbed volumes, we look for registry entries
        # under all possible USB bus which have a "BSD Name" that starts with "disk"
        # (i.e. this is a USB disk), and have a IORegistryEntryName that
        # matches /\cmbed/
        # Once we've found a disk, we can search up for a parent with a valid
        # serial number, and then search down again to find a tty that's part
        # of the same composite device
        # ioreg -a -r -n <usb_controller_name> -l
        usb_controllers = ['AppleUSBXHCI', 'AppleUSBUHCI', 'AppleUSBEHCI', 'AppleUSBOHCI', 'IOUSBHostDevice']
        usb_bus = []

        # For El Captain we need to list all the instances of (-c) rather than compare names (-n)
        mac_ver = float('.'.join(platform.mac_ver()[0].split('.')[:2])) # Returns mac version as float XX.YY
        cmp_par = '-c' if mac_ver >= 10.11 else '-n'

        for usb_controller in usb_controllers:
            ioreg_usb = subprocess.Popen(['ioreg', '-a', '-r', cmp_par, usb_controller, '-l'], stdout=subprocess.PIPE)

	    try:
                usb_bus = usb_bus + plistlib.readPlist(ioreg_usb.stdout)
	    except:
		# Catch when no output is returned from ioreg command
                pass

            ioreg_usb.wait()

        r = {}

        def findTTYRecursive(obj):
            ''' return the first tty (AKA IODialinDevice) that we can find in the
                children of the specified object, or None if no tty is present.
            '''
            if 'IODialinDevice' in obj:
                return obj['IODialinDevice']
            if 'IORegistryEntryChildren' in obj:
                for child in obj['IORegistryEntryChildren']:
                    found = findTTYRecursive(child)
                    if found:
                        return found
            return None

        def findVolumesRecursive(obj, parents):
            if 'BSD Name' in obj and obj['BSD Name'].startswith('disk') and \
                    self.mbed_volume_name_match.search(obj['IORegistryEntryName']):
                disk_id = obj['BSD Name']
                # now search up through our parents until we find a serial number:
                usb_info = {
                        'serial':None,
                     'vendor_id':None,
                    'product_id':None,
                           'tty':None,
                }
                for parent in [obj] + parents:
                    if 'USB Serial Number' in parent:
                        usb_info['serial'] = parent['USB Serial Number']
                    if 'idVendor' in parent and 'idProduct' in parent:
                        usb_info['vendor_id'] = parent['idVendor']
                        usb_info['product_id'] = parent['idProduct']
                    if usb_info['serial']:
                        # stop at the first one we find (or we'll pick up hubs,
                        # etc.), but first check for a tty that's also a child of
                        # this device:
                        usb_info['tty'] = findTTYRecursive(parent)
                        break
                r[disk_id] = usb_info
            if 'IORegistryEntryChildren' in obj:
                for child in obj['IORegistryEntryChildren']:
                    findVolumesRecursive(child, [obj] + parents)

        for obj in usb_bus:
            findVolumesRecursive(obj, [])

        return r
