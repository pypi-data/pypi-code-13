class AppWall661Meta(object):
    def __init__(self):
        self.interfaceIpEntry = self.InterfaceIpEntry()
        self.serviceIfacesEntry = self.ServiceIfacesEntry()
        self.platform = self.Platform()
        self.charsetEntry = self.CharsetEntry()
        self.restoreServiceBackupAction = self.RestoreServiceBackupAction()
        self.license = self.License()
        self.restartStatus = self.RestartStatus()
        self.securityTargetAddressesEntry = self.SecurityTargetAddressesEntry()
        self.managementRoutesEntry = self.ManagementRoutesEntry()
        self.certificatesEntry = self.CertificatesEntry()
        self.geoIPEntry = self.GeoIPEntry()
        self.restoreApplianceBackupAction = self.RestoreApplianceBackupAction()
        self.enableLag = self.EnableLag()
        self.systemTargetAddressesEntry = self.SystemTargetAddressesEntry()
        self.setAppwallServiceStatusAction = self.SetAppwallServiceStatusAction()
        self.ntpServerName = self.NtpServerName()
        self.bondDeployAction = self.BondDeployAction()
        self.timeStamp = self.TimeStamp()
        self.ntpServerStatus = self.NtpServerStatus()
        self.checkIPGroupsAction = self.CheckIPGroupsAction()
        self.enableSysLog = self.EnableSysLog()
        self.parametersSecurityBypassEntry = self.ParametersSecurityBypassEntry()
        self.appwallServiceStatus = self.AppwallServiceStatus()
        self.countriesEntry = self.CountriesEntry()
        self.createCertificateEntry = self.CreateCertificateEntry()
        self.syslogMaxMessageSize = self.SyslogMaxMessageSize()
        self.consoleListenerEntry = self.ConsoleListenerEntry()
        self.deleteApplianceBackupAction = self.DeleteApplianceBackupAction()
        self.serviceBackupsEntry = self.ServiceBackupsEntry()
        self.appwallType = self.AppwallType()
        self.formFactor = self.FormFactor()
        self.parsingPropertiesEntry = self.ParsingPropertiesEntry()
        self.commHostsEntry = self.CommHostsEntry()
        self.showRoutingTableRpdb = self.ShowRoutingTableRpdb()
        self.lastChangeTime = self.LastChangeTime()
        self.exportLicenseAction = self.ExportLicenseAction()
        self.setDateTimeAction = self.SetDateTimeAction()
        self.radiusServersEntry = self.RadiusServersEntry()
        self.enableNtpServer = self.EnableNtpServer()
        self.customMessagesEntry = self.CustomMessagesEntry()
        self.serverHeaderEntry = self.ServerHeaderEntry()
        self.upgradeAction = self.UpgradeAction()
        self.eventsInit = self.EventsInit()
        self.dNSEntry = self.DNSEntry()
        self.type = self.Type()
        self.aDStatus = self.ADStatus()
        self.secHostsEntry = self.SecHostsEntry()
        self.ntpDate = self.NtpDate()
        self.initStatus = self.InitStatus()
        self.fileTypeSecurityBypassEntry = self.FileTypeSecurityBypassEntry()
        self.appwallVersion = self.AppwallVersion()
        self.name = self.Name()
        self.serviceStartTimeLast = self.ServiceStartTimeLast()
        self.applianceBackupsEntry = self.ApplianceBackupsEntry()
        self.version = self.Version()
        self.build = self.Build()
        self.loggedinUser = self.LoggedinUser()
        self.interfacesEntry = self.InterfacesEntry()
        self.iPRangesEntry = self.IPRangesEntry()
        self.hostName = self.HostName()
        self.clusterNode = self.ClusterNode()
        self.adaptersEntry = self.AdaptersEntry()
        self.checkSysLogServerAction = self.CheckSysLogServerAction()
        self.allowEmptyLogin = self.AllowEmptyLogin()
        self.licenseHostId = self.LicenseHostId()
        self.webAppWizardEntry = self.WebAppWizardEntry()
        self.clusterTunnelsEntry = self.ClusterTunnelsEntry()
        self.httpTunnelsEntry = self.HttpTunnelsEntry()
        self.customHeadersEntry = self.CustomHeadersEntry()
        self.secTunnelsEntry = self.SecTunnelsEntry()
        self.applicationPathEntry = self.ApplicationPathEntry()
        self.upgradeImagesEntry = self.UpgradeImagesEntry()
        self.httpsTunnelsEntry = self.HttpsTunnelsEntry()
        self.createServiceBackupAction = self.CreateServiceBackupAction()
        self.operatingSystem = self.OperatingSystem()
        self.allTunnelsEntry = self.AllTunnelsEntry()
        self.serverType = self.ServerType()
        self.userAccessTableEntry = self.UserAccessTableEntry()
        self.checkWebServerAction = self.CheckWebServerAction()
        self.enslaveNamesEntry = self.EnslaveNamesEntry()
        self.enslavesEntry = self.EnslavesEntry()
        self.visiondrivername = self.visiondrivername()
        self.applyStatus = self.ApplyStatus()
        self.isBridge = self.IsBridge()
        self.sysLogDestinationEntry = self.SysLogDestinationEntry()
        self.usersEntry = self.UsersEntry()
        self.clusterNodesStatusEntry = self.ClusterNodesStatusEntry()
        self.checkRadiusServerAction = self.CheckRadiusServerAction()
        self.empty = self.Empty()
        self.defaultServiceRoute = self.DefaultServiceRoute()
        self.iPGroupsEntry = self.IPGroupsEntry()
        self.systemUpTime = self.SystemUpTime()
        self.webAppsEntry = self.WebAppsEntry()
        self.createApplianceBackupAction = self.CreateApplianceBackupAction()
        self.syslogForwardingAddress = self.SyslogForwardingAddress()
        self.currentStatus = self.CurrentStatus()
        self.bondUndeployAction = self.BondUndeployAction()
        self.exportTunnelAction = self.ExportTunnelAction()
        self.bondsEntry = self.BondsEntry()
        self.nodesAdaptersEntry = self.NodesAdaptersEntry()
        self.serviceRoutesEntry = self.ServiceRoutesEntry()
        self.defaultManagementRoute = self.DefaultManagementRoute()
        self.licensesEntry = self.LicensesEntry()
        self.webServersEntry = self.WebServersEntry()
        self.serviceLastStarted = self.ServiceLastStarted()
        self.iPMasksEntry = self.IPMasksEntry()
        self.clusterNodeEntry = self.ClusterNodeEntry()

    class InterfaceIpEntry:
        def __init__(self):
            self.name = 'name'
            self.iP = 'iP'
            self.mask = 'mask'

        def __call__(self):
            return 'InterfaceIpEntry'

    class ServiceIfacesEntry:
        def __init__(self):
            self._interface = '_interface'

        def __call__(self):
            return 'ServiceIfacesEntry'

    class Platform:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'Platform'

    class CharsetEntry:
        def __init__(self):
            self.address = 'address'

        def __call__(self):
            return 'CharsetEntry'

    class RestoreServiceBackupAction:
        def __init__(self):
            self.name = 'name'

        def __call__(self):
            return 'RestoreServiceBackupAction'

    class License:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'License'

    class RestartStatus:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'RestartStatus'

    class SecurityTargetAddressesEntry:
        def __init__(self):
            self.address = 'address'
            self.port = 'port'
            self.version = 'version'

        def __call__(self):
            return 'SecurityTargetAddressesEntry'

    class ManagementRoutesEntry:
        def __init__(self):
            self.network = 'network'
            self.networkPrefix = 'networkPrefix'
            self.gateway = 'gateway'

        def __call__(self):
            return 'ManagementRoutesEntry'

    class CertificatesEntry:
        def __init__(self):
            self.name = 'name'
            self.issuedBy = 'issuedBy'
            self.issuedTo = 'issuedTo'
            self.endDate = 'endDate'
            self.serialNumber = 'serialNumber'

        def __call__(self):
            return 'CertificatesEntry'

    class GeoIPEntry:
        def __init__(self):
            self.name = 'name'
            self.geo = 'geo'
            self.exclude = 'exclude'

        def __call__(self):
            return 'GeoIPEntry'

    class RestoreApplianceBackupAction:
        def __init__(self):
            self.name = 'name'

        def __call__(self):
            return 'RestoreApplianceBackupAction'

    class EnableLag:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'EnableLag'

    class SystemTargetAddressesEntry:
        def __init__(self):
            self.address = 'address'
            self.port = 'port'
            self.version = 'version'

        def __call__(self):
            return 'SystemTargetAddressesEntry'

    class SetAppwallServiceStatusAction:
        def __init__(self):
            self.status = 'status'

        def __call__(self):
            return 'SetAppwallServiceStatusAction'

    class NtpServerName:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'NtpServerName'

    class BondDeployAction:
        def __init__(self):
            self.name = 'name'

        def __call__(self):
            return 'BondDeployAction'

    class TimeStamp:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'TimeStamp'

    class NtpServerStatus:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'NtpServerStatus'

    class CheckIPGroupsAction:
        def __init__(self):
            self.name = 'name'
            self.testIP = 'testIP'

        def __call__(self):
            return 'CheckIPGroupsAction'

    class EnableSysLog:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'EnableSysLog'

    class ParametersSecurityBypassEntry:
        def __init__(self):
            self.tunnelName = 'tunnelName'
            self.parameter = 'parameter'

        def __call__(self):
            return 'ParametersSecurityBypassEntry'

    class AppwallServiceStatus:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'AppwallServiceStatus'

    class CountriesEntry:
        def __init__(self):
            self.code = 'code'
            self.value = 'value'
            self.countries = 'countries'

        def __call__(self):
            return 'CountriesEntry'

    class CreateCertificateEntry:
        def __init__(self):
            self.name = 'name'

        def __call__(self):
            return 'CreateCertificateEntry'

    class SyslogMaxMessageSize:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'SyslogMaxMessageSize'

    class ConsoleListenerEntry:
        def __init__(self):
            self.serverConnectionType = 'serverConnectionType'
            self.iP = 'iP'
            self.port = 'port'
            self.maximumRemoteConnections = 'maximumRemoteConnections'
            self.connectedSecurityConsoles = 'connectedSecurityConsoles'
            self.useanEncryptedConnection = 'useanEncryptedConnection'

        def __call__(self):
            return 'ConsoleListenerEntry'

    class DeleteApplianceBackupAction:
        def __init__(self):
            self.name = 'name'

        def __call__(self):
            return 'DeleteApplianceBackupAction'

    class ServiceBackupsEntry:
        def __init__(self):
            self.directoryName = 'directoryName'
            self.date = 'date'

        def __call__(self):
            return 'ServiceBackupsEntry'

    class AppwallType:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'AppwallType'

    class FormFactor:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'FormFactor'

    class ParsingPropertiesEntry:
        def __init__(self):
            self.tunnelName = 'tunnelName'
            self.uRL = 'uRL'
            self.disableJsonParsing = 'disableJsonParsing'
            self.parameterEqualSign = 'parameterEqualSign'
            self.parameterWithoutValue = 'parameterWithoutValue'

        def __call__(self):
            return 'ParsingPropertiesEntry'

    class CommHostsEntry:
        def __init__(self):
            self.tunnelName = 'tunnelName'
            self.hostName = 'hostName'

        def __call__(self):
            return 'CommHostsEntry'

    class ShowRoutingTableRpdb:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'ShowRoutingTableRpdb'

    class LastChangeTime:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'LastChangeTime'

    class ExportLicenseAction:
        def __init__(self):
            self.index = 'index'

        def __call__(self):
            return 'ExportLicenseAction'

    class SetDateTimeAction:
        def __init__(self):
            self.time = 'time'

        def __call__(self):
            return 'SetDateTimeAction'

    class RadiusServersEntry:
        def __init__(self):
            self.serverName = 'serverName'
            self.primaryHost = 'primaryHost'
            self.primaryPort = 'primaryPort'
            self.primarySecret = 'primarySecret'
            self.secondaryHost = 'secondaryHost'
            self.secondaryPort = 'secondaryPort'
            self.secondarySecret = 'secondarySecret'
            self.timeout = 'timeout'
            self.retries = 'retries'
            self.usernameForTesting = 'usernameForTesting'
            self.passwordForTesting = 'passwordForTesting'
            self.forceManagmentIP = 'forceManagmentIP'
            self.subSystem = 'subSystem'

        def __call__(self):
            return 'RadiusServersEntry'

    class EnableNtpServer:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'EnableNtpServer'

    class CustomMessagesEntry:
        def __init__(self):
            self.tunnelName = 'tunnelName'
            self.statusCodeRangeFrom = 'statusCodeRangeFrom'
            self.statusCodeRangeTo = 'statusCodeRangeTo'
            self.messageBody = 'messageBody'
            self.fileName = 'fileName'

        def __call__(self):
            return 'CustomMessagesEntry'

    class ServerHeaderEntry:
        def __init__(self):
            self.header = 'header'

        def __call__(self):
            return 'ServerHeaderEntry'

    class UpgradeAction:
        def __init__(self):
            self.name = 'name'

        def __call__(self):
            return 'UpgradeAction'

    class EventsInit:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'EventsInit'

    class DNSEntry:
        def __init__(self):
            self.iP = 'iP'

        def __call__(self):
            return 'DNSEntry'

    class Type:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'Type'

    class ADStatus:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'ADStatus'

    class SecHostsEntry:
        def __init__(self):
            self.webAppName = 'webAppName'
            self.tunnelName = 'tunnelName'
            self.hostName = 'hostName'
            self.securityPage = 'securityPage'

        def __call__(self):
            return 'SecHostsEntry'

    class NtpDate:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'NtpDate'

    class InitStatus:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'InitStatus'

    class FileTypeSecurityBypassEntry:
        def __init__(self):
            self.tunnelName = 'tunnelName'
            self.extension = 'extension'

        def __call__(self):
            return 'FileTypeSecurityBypassEntry'

    class AppwallVersion:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'AppwallVersion'

    class Name:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'Name'

    class ServiceStartTimeLast:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'ServiceStartTimeLast'

    class ApplianceBackupsEntry:
        def __init__(self):
            self.fileName = 'fileName'

        def __call__(self):
            return 'ApplianceBackupsEntry'

    class Version:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'Version'

    class Build:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'Build'

    class LoggedinUser:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'LoggedinUser'

    class InterfacesEntry:
        def __init__(self):
            self.name = 'name'
            self.mac = 'mac'
            self.linkOn = 'linkOn'

        def __call__(self):
            return 'InterfacesEntry'

    class IPRangesEntry:
        def __init__(self):
            self.name = 'name'
            self._from = 'from'
            self.to = 'to'
            self.exclude = 'exclude'

        def __call__(self):
            return 'IPRangesEntry'

    class HostName:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'HostName'

    class ClusterNode:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'ClusterNode'

    class AdaptersEntry:
        def __init__(self):
            self.address = 'address'

        def __call__(self):
            return 'AdaptersEntry'

    class CheckSysLogServerAction:
        def __init__(self):
            self.iP = 'iP'

        def __call__(self):
            return 'CheckSysLogServerAction'

    class AllowEmptyLogin:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'AllowEmptyLogin'

    class LicenseHostId:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'LicenseHostId'

    class WebAppWizardEntry:
        def __init__(self):
            self.webAppName = 'webAppName'
            self.tunnelName = 'tunnelName'
            self.hostName = 'hostName'
            self.applicationPath = 'applicationPath'
            self.securityPage = 'securityPage'

        def __call__(self):
            return 'WebAppWizardEntry'

    class ClusterTunnelsEntry:
        def __init__(self):
            self.nodeName = 'nodeName'
            self.nodeStatus = 'nodeStatus'
            self.tunnelName = 'tunnelName'
            self.tunnelStatus = 'tunnelStatus'
            self.listenAddress = 'listenAddress'
            self.listenPort = 'listenPort'
            self.forwardAddress = 'forwardAddress'
            self.protocol = 'protocol'

        def __call__(self):
            return 'ClusterTunnelsEntry'

    class HttpTunnelsEntry:
        def __init__(self):
            self.name = 'name'
            self.tunnelMode = 'tunnelMode'
            self.listenAddress = 'listenAddress'
            self.listenPort = 'listenPort'
            self.forwardingAddress = 'forwardingAddress'
            self.idleSession = 'idleSession'
            self.protectedType = 'protectedType'
            self.serverName = 'serverName'
            self.status = 'status'
            self.operationalMode = 'operationalMode'
            self.failureHandling = 'failureHandling'
            self.pendingConnections = 'pendingConnections'
            self.activeConnections = 'activeConnections'
            self.xForwarded = 'xForwarded'
            self.codepageEncoding = 'codepageEncoding'
            self.allowMessageParameterValues = 'allowMessageParameterValues'
            self.sessionDelimeter = 'sessionDelimeter'
            self.uRLQueryDelimeter = 'uRLQueryDelimeter'
            self.parameterDelimeter = 'parameterDelimeter'
            self.codepageEncodingScheme = 'codepageEncodingScheme'
            self.enableCustomHeaders = 'enableCustomHeaders'
            self.enableProtectionSlowloris = 'enableProtectionSlowloris'
            self.checksTimeGap = 'checksTimeGap'
            self.minimalSentDataAmount = 'minimalSentDataAmount'
            self.enableServerIdentity = 'enableServerIdentity'
            self.serverIdentity = 'serverIdentity'
            self.headerValues = 'headerValues'

        def __call__(self):
            return 'HttpTunnelsEntry'

    class CustomHeadersEntry:
        def __init__(self):
            self.tunnelName = 'tunnelName'
            self.headerName = 'headerName'
            self.delimiter = 'delimiter'
            self.freeText = 'freeText'
            self.sessionDateTime = 'sessionDateTime'
            self.messageDateTime = 'messageDateTime'
            self.clientPort = 'clientPort'
            self.clientIP = 'clientIP'
            self.forwardingPort = 'forwardingPort'
            self.forwardingIP = 'forwardingIP'

        def __call__(self):
            return 'CustomHeadersEntry'

    class SecTunnelsEntry:
        def __init__(self):
            self.webAppName = 'webAppName'
            self.tunnelName = 'tunnelName'

        def __call__(self):
            return 'SecTunnelsEntry'

    class ApplicationPathEntry:
        def __init__(self):
            self.webAppName = 'webAppName'
            self.tunnelName = 'tunnelName'
            self.hostName = 'hostName'
            self.vDName = 'vDName'
            self.forceToSuccessive = 'forceToSuccessive'
            self.vulnerabilities = 'vulnerabilities'
            self.database = 'database'
            self.hTTPMethods = 'hTTPMethods'
            self.safeReply = 'safeReply'
            self.session = 'session'
            self.allowList = 'allowList'
            self.pathBlocking = 'pathBlocking'
            self.logging = 'logging'
            self.filesUpload = 'filesUpload'
            self.webServices = 'webServices'
            self.parameters = 'parameters'
            self.xMLSecurity = 'xMLSecurity'
            self.globalParameters = 'globalParameters'
            self.bruteForce = 'bruteForce'

        def __call__(self):
            return 'ApplicationPathEntry'

    class UpgradeImagesEntry:
        def __init__(self):
            self.fileName = 'fileName'

        def __call__(self):
            return 'UpgradeImagesEntry'

    class HttpsTunnelsEntry:
        def __init__(self):
            self.name = 'name'
            self.tunnelMode = 'tunnelMode'
            self.listenAddress = 'listenAddress'
            self.listenPort = 'listenPort'
            self.forwardingAddress = 'forwardingAddress'
            self.idleSession = 'idleSession'
            self.sSLMode = 'sSLMode'
            self.protectedType = 'protectedType'
            self.serverName = 'serverName'
            self.selectedCertificate = 'selectedCertificate'
            self.status = 'status'
            self.operationalMode = 'operationalMode'
            self.failureHandling = 'failureHandling'
            self.pendingConnections = 'pendingConnections'
            self.activeConnections = 'activeConnections'
            self.xForwarded = 'xForwarded'
            self.codepageEncoding = 'codepageEncoding'
            self.allowMessageParameterValues = 'allowMessageParameterValues'
            self.sessionDelimeter = 'sessionDelimeter'
            self.uRLQueryDelimeter = 'uRLQueryDelimeter'
            self.parameterDelimeter = 'parameterDelimeter'
            self.codepageEncodingScheme = 'codepageEncodingScheme'
            self.enableCustomHeaders = 'enableCustomHeaders'
            self.enableProtectionSlowloris = 'enableProtectionSlowloris'
            self.checksTimeGap = 'checksTimeGap'
            self.minimalSentDataAmount = 'minimalSentDataAmount'
            self.enableServerIdentity = 'enableServerIdentity'
            self.serverIdentity = 'serverIdentity'
            self.headerValues = 'headerValues'

        def __call__(self):
            return 'HttpsTunnelsEntry'

    class CreateServiceBackupAction:
        def __init__(self):
            self.name = 'name'

        def __call__(self):
            return 'CreateServiceBackupAction'

    class OperatingSystem:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'OperatingSystem'

    class AllTunnelsEntry:
        def __init__(self):
            self.name = 'name'

        def __call__(self):
            return 'AllTunnelsEntry'

    class ServerType:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'ServerType'

    class UserAccessTableEntry:
        def __init__(self):
            self.user = 'user'
            self.password = 'password'

        def __call__(self):
            return 'UserAccessTableEntry'

    class CheckWebServerAction:
        def __init__(self):
            self.name = 'name'
            self.iP = 'iP'

        def __call__(self):
            return 'CheckWebServerAction'

    class EnslaveNamesEntry:
        def __init__(self):
            self.ethName = 'ethName'

        def __call__(self):
            return 'EnslaveNamesEntry'

    class EnslavesEntry:
        def __init__(self):
            self.bondName = 'bondName'
            self.enslaveName = 'enslaveName'
            self.linkOn = 'linkOn'

        def __call__(self):
            return 'EnslavesEntry'

    class visiondrivername:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'visiondrivername'

    class ApplyStatus:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'ApplyStatus'

    class IsBridge:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'IsBridge'

    class SysLogDestinationEntry:
        def __init__(self):
            self.address = 'address'
            self.port = 'port'

        def __call__(self):
            return 'SysLogDestinationEntry'

    class UsersEntry:
        def __init__(self):
            self.login_Name = 'login_Name'
            self.group = 'group'
            self.type = 'type'
            self.radiusServer = 'radiusServer'
            self.radiusUserName = 'radiusUserName'
            self.status = 'status'
            self.yourPassword = 'yourPassword'
            self.newPassword = 'newPassword'

        def __call__(self):
            return 'UsersEntry'

    class ClusterNodesStatusEntry:
        def __init__(self):
            self.name = 'name'
            self.status = 'status'

        def __call__(self):
            return 'ClusterNodesStatusEntry'

    class CheckRadiusServerAction:
        def __init__(self):
            self.name = 'name'

        def __call__(self):
            return 'CheckRadiusServerAction'

    class Empty:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'Empty'

    class DefaultServiceRoute:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'DefaultServiceRoute'

    class IPGroupsEntry:
        def __init__(self):
            self.name = 'name'
            self.summary = 'summary'
            self.allowedBotIPs = 'allowedBotIPs'
            self.blackListedBotIPS = 'blackListedBotIPS'

        def __call__(self):
            return 'IPGroupsEntry'

    class SystemUpTime:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'SystemUpTime'

    class WebAppsEntry:
        def __init__(self):
            self.webAppName = 'webAppName'

        def __call__(self):
            return 'WebAppsEntry'

    class CreateApplianceBackupAction:
        def __init__(self):
            self.name = 'name'

        def __call__(self):
            return 'CreateApplianceBackupAction'

    class SyslogForwardingAddress:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'SyslogForwardingAddress'

    class CurrentStatus:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'CurrentStatus'

    class BondUndeployAction:
        def __init__(self):
            self.name = 'name'

        def __call__(self):
            return 'BondUndeployAction'

    class ExportTunnelAction:
        def __init__(self):
            self.tunnelName = 'tunnelName'

        def __call__(self):
            return 'ExportTunnelAction'

    class BondsEntry:
        def __init__(self):
            self.bondName = 'bondName'
            self.bondUp = 'bondUp'
            self.bondError = 'bondError'
            self.ad_select = 'ad_select'
            self.slaves_mode = 'slaves_mode'
            self.arp_validate = 'arp_validate'
            self.arp_all = 'arp_all'
            self.fail_over = 'fail_over'
            self.lacp_rate = 'lacp_rate'
            self.mode = 'mode'
            self.primary_reselect = 'primary_reselect'
            self.use_carrier = 'use_carrier'
            self.xmit_hash = 'xmit_hash'
            self.actionErrors = 'actionErrors'
            self.active_slave = 'active_slave'
            self.arp_interval = 'arp_interval'
            self.arp_ip_target = 'arp_ip_target'
            self.downdelay = 'downdelay'
            self.miimon = 'miimon'
            self.min_links = 'min_links'
            self.packets_per_slave = 'packets_per_slave'
            self.primary = 'primary'
            self.updelay = 'updelay'
            self.lp_interval = 'lp_interval'

        def __call__(self):
            return 'BondsEntry'

    class NodesAdaptersEntry:
        def __init__(self):
            self.address = 'address'

        def __call__(self):
            return 'NodesAdaptersEntry'

    class ServiceRoutesEntry:
        def __init__(self):
            self.network = 'network'
            self.networkPrefix = 'networkPrefix'
            self.gateway = 'gateway'
            self._interface = '_interface'

        def __call__(self):
            return 'ServiceRoutesEntry'

    class DefaultManagementRoute:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'DefaultManagementRoute'

    class LicensesEntry:
        def __init__(self):
            self.index = 'index'
            self.appWallService = 'appWallService'
            self.authentcatedLicense = 'authentcatedLicense'
            self.version = 'version'
            self.expirationDays = 'expirationDays'
            self.licenseType = 'licenseType'

        def __call__(self):
            return 'LicensesEntry'

    class WebServersEntry:
        def __init__(self):
            self.webServerName = 'webServerName'
            self.description = 'description'
            self.iP = 'iP'
            self.port = 'port'
            self.protocol = 'protocol'
            self.supportSSLv2 = 'supportSSLv2'
            self.supportSSLv3 = 'supportSSLv3'
            self.supportTLSv10 = 'supportTLSv10'
            self.supportTLSv11 = 'supportTLSv11'
            self.supportTLSv12 = 'supportTLSv12'

        def __call__(self):
            return 'WebServersEntry'

    class ServiceLastStarted:
        def __init__(self):
            self.value = 'value'

        def __call__(self):
            return 'ServiceLastStarted'

    class IPMasksEntry:
        def __init__(self):
            self.name = 'name'
            self.iP = 'iP'
            self.mask = 'mask'
            self.exclude = 'exclude'

        def __call__(self):
            return 'IPMasksEntry'

    class ClusterNodeEntry:
        def __init__(self):
            self.name = 'name'
            self.iP = 'iP'
            self.port = 'port'
            self.userName = 'userName'
            self.password = 'password'
            self.sSL = 'sSL'
            self.defaultIP = 'defaultIP'
            self.initializationStatus = 'initializationStatus'

        def __call__(self):
            return 'ClusterNodeEntry'


