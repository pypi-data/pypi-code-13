import re
from ssh import SSHSession


class GenericLinuxServer(SSHSession):
    """
    Establish SSH connection to Linux based server and run commands.
    """
    @property
    def hostname(self):
        """
        Returns Server Hostname
        """
        output, error = self.command('hostname')
        return " ".join(output).strip()


class RedHatServer(GenericLinuxServer):
    """
    Establish SSH connection to RedHat Server and retrieve information
    """
    @property
    def has_hba(self):
        """
        Return True if Server has HBA's, otherwise False
        """
        output, error = self.command('/sbin/lspci | grep -i fibre')
        if output:
            return True
        else:
            return False

    @property
    def hba_manufacturer(self):
        """
        Returns HBA Manufacturer
        """
        manufacturer = None
        if self.has_hba:
            output, error = self.command('/sbin/lspci | grep -i fibre')
            if re.search("Brocade", " ".join(output), re.IGNORECASE) and not re.search("QLogic|Emulex", " ".join(output), re.IGNORECASE):
                manufacturer = "Brocade"
            elif re.search("QLogic", " ".join(output), re.IGNORECASE) and not re.search("Brocade|Emulex", " ".join(output), re.IGNORECASE):
                manufacturer = "QLogic"
            elif re.search("QLogic", " ".join(output), re.IGNORECASE) and not re.search("Brocade|QLogic", " ".join(output), re.IGNORECASE):
                manufacturer = "Emulex"
            else:
                manufacturer = "Unknown"
        return manufacturer

    @property
    def wwpns(self):
        """
        Returns WWPN's as list
        """
        wwpn_list = []

        if self.hba_manufacturer:
            output, error = self.command('cat /sys/class/fc_host/host*/port_name')
            if output and not re.search('No such file or directory', " ".join(output), re.IGNORECASE):
                for item in output:
                    item = item.strip()
                    if re.match("0x", item) and len(item) == 18:
                        wwpn_list.append(":".join(re.findall('..', item.replace('0x', '', 1))))
                    else:
                        pass
        return wwpn_list


class ESXServer(GenericLinuxServer):
    """
    Establish SSH connection to ESX Server and retrieve information
    """
    @property
    def has_hba(self):
        """
        Return True if Server has HBA's, otherwise False
        """
        output, error = self.command('/sbin/lspci | grep -i fibre')
        if output:
            return True
        else:
            return False

    @property
    def hba_manufacturer(self):
        """
        Returns HBA Manufacturer
        """
        manufacturer = None
        if self.has_hba:
            output, error = self.command('/sbin/lspci | grep -i fibre')
            if re.search("Brocade", " ".join(output), re.IGNORECASE) and not re.search("QLogic|Emulex", " ".join(output), re.IGNORECASE):
                manufacturer = "Brocade"
            elif re.search("QLogic", " ".join(output), re.IGNORECASE) and not re.search("Brocade|Emulex", " ".join(output), re.IGNORECASE):
                manufacturer = "QLogic"
            elif re.search("QLogic", " ".join(output), re.IGNORECASE) and not re.search("Brocade|QLogic", " ".join(output), re.IGNORECASE):
                manufacturer = "Emulex"
            else:
                manufacturer = "Unknown"
        return manufacturer

    @property
    def wwpns(self):
        """
        Returns a list with WWPN's
        """
        wwpn_list = []
        manufacturer = self.hba_manufacturer
        if manufacturer:
            if manufacturer == "Brocade":
                output, error = self.command('cat /proc/scsi/bfa/* | grep WWPN')
                if output and not re.search('No such file or directory', " ".join(output), re.IGNORECASE):
                    for item in output:
                        item = item.strip()
                        if re.match("WWPN: ", item) and len(item) == 29:
                            wwpn_list.append(item.strip("WWPN: "))
            elif manufacturer == "QLogic":
                output, error = self.command('cat /proc/scsi/qla2xxx/* | grep adapter-port')
                if output and not re.search('No such file or directory', " ".join(output), re.IGNORECASE):
                    for item in output:
                        item = item.strip()
                        if re.match('scsi-qla.+-adapter-port=[A-Fa-f0-9]{16}:', item):
                            wwpn = re.match('scsi-qla.+-adapter-port=[A-Fa-f0-9]{16}:', item).group().split('=')[
                                   1].strip(':')
                            wwpn_list.append(":".join(re.findall('..', wwpn)))
        return wwpn_list


class ESXiServer(GenericLinuxServer):
    """
    Establish SSH connection to ESXi Server and retrieve information
    """
    @property
    def has_hba(self):
        """
        Return True if Server has HBA's, otherwise False
        """
        output, error = self.command('/sbin/lspci | grep -i vmhba')
        if output:
            return True
        else:
            return False

    @property
    def hba_manufacturer(self):
        """
        Returns HBA Manufacturer
        """
        manufacturer = None
        if self.has_hba:
            output, error = self.command('/sbin/lspci | grep -i vmhba')
            if re.search("Brocade", " ".join(output), re.IGNORECASE) and not re.search("QLogic|Emulex", " ".join(output), re.IGNORECASE):
                manufacturer = "Brocade"
            elif re.search("QLogic", " ".join(output), re.IGNORECASE) and not re.search("Brocade|Emulex", " ".join(output), re.IGNORECASE):
                manufacturer = "QLogic"
            elif re.search("QLogic", " ".join(output), re.IGNORECASE) and not re.search("Brocade|QLogic", " ".join(output), re.IGNORECASE):
                manufacturer = "Emulex"
            else:
                manufacturer = "Unknown"
        return manufacturer

    @property
    def wwpns(self):
        """
        Returns a list with WWPN's
        """
        wwpn_list = []
        manufacturer = self.hba_manufacturer
        if manufacturer:
            if manufacturer == "Brocade":
                output, error = self.command('cat /proc/scsi/bfa/* | grep WWPN')
                if output and not re.search('No such file or directory', " ".join(output), re.IGNORECASE):
                    for item in output:
                        item = item.strip()
                        if re.match("WWPN: ", item) and len(item) == 29:
                            wwpn_list.append(item.strip("WWPN: "))
            elif manufacturer == "QLogic":
                output, error = self.command('cat /proc/scsi/qla2xxx/* | grep adapter-port')
                if output and not re.search('No such file or directory', " ".join(output), re.IGNORECASE):
                    for item in output:
                        item = item.strip()
                        if re.match('scsi-qla.+-adapter-port=[A-Fa-f0-9]{16}:', item):
                            wwpn = re.match('scsi-qla.+-adapter-port=[A-Fa-f0-9]{16}:', item).group().split('=')[
                                   1].strip(':')
                            wwpn_list.append(":".join(re.findall('..', wwpn)))
        return wwpn_list
