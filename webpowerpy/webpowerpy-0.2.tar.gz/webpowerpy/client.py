# -*- coding: utf-8 -*-
#from zeep import Client
from suds.client import Client

from .conf import *
from .exceptions import *

DEFAULT_GROUP_ID = 1

class WebPowerClient(object):

    def __init__(self, wsdl, username, password):

        self.client = Client(wsdl)

        #Create and initialize login parameter
        self.login = self.client.factory.create('ns0:WebpowerLoginType')
        setattr(self.login,'username', username)
        setattr(self.login,'password', password)

    def addEventAttendee(self, campaignID, eventID, recipientData, status):
        '''
        Add or update an attendee for a specified event.
        Returns: original attendee data with extra fields eventResponse
           and eventMessage.
        '''
        raise NotImplementedError

    def addGroup(self, campaignID, group):
        '''
        Add a new group to this DMdelivery campaign.
        Required credentials: 'insert' privilege for area 'Groups'
        Returns: The database ID of the newly created group.
        '''
        raise NotImplementedError

    def addNotification(self, title, body, severity, source, expireDate):
        '''
        Add a notification to the dashboard of DMdelivery.
        Required credentials: a valid user, no special privileges are required.
        Returns: A unique ID (integer) for the new notification.
        '''
        raise NotImplementedError

    def addOverallRecipient(self, campaignIDs, groupIDs, recipientData,
            overwrite):
        '''
        Add a new recipient to the overall DMdelivery database.
        Required credentials: 'insert' privilege for area 'Overall recipients'
        Returns: The database ID of the newly created recipient.
        '''
        raise NotImplementedError

    def addOverallRecipientToGroups(self, campaignIDs, recipientID,
            groupIDs):
        '''
        Make an overall recipient a member of one or more groups in one or
        more overall campaigns.
        Returns: true.
        '''
        raise NotImplementedError

    def addRecipient(self, campaignID, groupIDs, recipientData,
            addDuplisToGroup=False, overwrite=False):
        '''
        campaignID: int
        groupIds: [int]
        recipientData: dict({key:value,})

        Add a new recipient to a DMdelivery campaign.
        Required credentials: 'insert' privilege for area 'Recipients'
        Returns: The database ID of the newly created recipient.
        '''
        #Create ArrayOfIntType and append default group id
        groups = self.client.factory.create('ns0:ArrayOfIntType')
        for group in groupIDs:
            groups.int.append(group)

        #Create NewRecipientType and populate with RecipientNameValuePairType
        recipient = self.client.factory.create('ns0:NewRecipientType')

        #Iterate over recieved data and populate NewRecipientType
        for key, value in recipientData.items():

            field = self.client.factory.create('ns0:RecipientNameValuePairType')
            field.name = key
            field.value = value

            recipient.fields.append(field)

        result = self.client.service.addRecipient(self.login,
            campaignID, groups, recipient, addDuplisToGroup, overwrite)
        return result

    def addRecipients(self, campaignID, groupIDs, recipientDatas,
            addDuplisToGroup=False, overwrite=False):
        '''
        campaignID: int
        groupIds: [int]
        recipientDatas: [dict({key:val, key:val}),dict({key:val, key:val})]

        Add multiple new recipients to DMdelivery (max 1000 at once).
        Required credentials: 'insert' privilege for area 'Recipients'
        Returns: Complex datatype, containing all successfully inserted records
            (including the ID assigned by DMdelivery), duplicates and/or errors.
        '''
        #Create ArrayOfIntType and append default group id
        groups = self.client.factory.create('ns0:ArrayOfIntType')
        for group in groupIDs:
            groups.int.append(group)

        #Create NewRecipientArrayType to list all recipients to add
        recipient_array = self.client.factory.create('ns0:NewRecipientArrayType')

        #Iterate over recieved list of dict, create and populate each recipient
        for data in recipientDatas:
            #Create and populate one recipient
            recipient = self.client.factory.create('ns0:NewRecipientType')
            for key, value in data.items():
                field = self.client.factory.create('ns0:RecipientNameValuePairType')
                field.name = key
                field.value = value
                recipient.fields.append(field)

            #Append created recipient to recipient_array
            recipient_array.recipients.append(recipient)


        result = self.client.service.addRecipients(self.login,
            campaignID, groups, recipient_array, addDuplisToGroup, overwrite)

        return result

    def addRecipientsSendMailing(self, campaignID, mailingID, groupIDs,
            recipientDatas, addDuplisToGroup, overwrite):
        '''
        Import recipients (max 1000 at once), while sending a (definitive)
        mailing to them. Required credentials: 'insert' privilege for area
        'Recipients' AND access to area 'Send mailing'.
        Returns: Complex datatype, containing all duplicates and/or errors.
        '''
        raise NotImplementedError

    def addRecipientsSendSMS(self, campaignID, SMSmailingID, groupIDs,
            recipientDatas, addDuplisToGroup, overwrite):
        '''
        Import recipients (max 1000 at once), while sending a (definitive)
        SMS to them. Required credentials: 'insert' privilege for area
        'Recipients' AND access to area 'Send mailing'
        Returns: Complex datatype, containing all duplicates and/or errors.
        '''
        raise NotImplementedError

    def addRecipientToGroups(self, campaignID, recipientID, groupIDs):
        '''
        Make a recipient a member of one or more groups.
        Required credentials: 'update' privilege for area 'Recipients'
        Returns: An array of groups (database IDs) the recipient is now a member of.
        '''
        raise NotImplementedError

    def checkHealth(self):
        '''
        Check the health of DMdelivery's webservice. Specifically: check
        whether the webservice is available (http(s) access), and the database
        is up and responsive.
        Returns: true, when health is okay.
        '''
        raise NotImplementedError

    def createMailing(self, campaignID, mailingName, lang, subject,
        fromName, senderID, html, preheader):
        '''
        Create a mailing from scratch, providing raw HTML.
        The plaintext-message is inherited from the campaign's default
        plaintext message. Required credentials: 'insert' privilege for area
        'Mailings'
        Returns: The database ID of the mailing that was created.
        '''
        raise NotImplementedError

    def deleteGroup(self, campaignID, groupID):
        '''
        Flush all recipients from a recipient group, then delete the group.
        The recipients are 'disconnected' from the group, not physically deleted.
        Afterwards, the group will no longer exist. Required credentials:
        'delete' privilege for area 'Groups'
        Returns: Number of groups (0 or 1) actually deleted.
        '''
        raise NotImplementedError

    def deleteMailing(self, campaignID, mailingID):
        '''
        Delete a mailing from a campaign.
        Required credentials: 'delete' privilege for area 'Mailings'
        Returns: 'OK' or 'ERROR'
        '''
        raise NotImplementedError

    def editOverallRecipient(self, campaignIDs, recipientID, groupIDs,
            recipientData):
        '''
        Edit the data of an existing overall recipient, enabling modifying
        campaign and/or group memberships. Required credentials: 'update'
        privilege for area 'Overall recipients'
        Returns: The database ID of the updated recipient.
        '''
        raise NotImplementedError

    def editRecipient(self, campaignID, recipientID, recipientData):
        '''
        campaignID = int
        recipientID = int
        recipientData = dict({key:value,})

        Edit the data of an existing recipient.
        Required credentials: 'update' privilege for area 'Recipients'
        Returns: The database ID of the updated recipient.
        '''

        #Create NewRecipientType and populate with RecipientNameValuePairType
        recipient_data = self.client.factory.create('ns0:NewRecipientType')

        #Iterate over recieved data and populate NewRecipientType
        for key, value in recipientData.items():

            field = self.client.factory.create('ns0:RecipientNameValuePairType')
            field.name = key
            field.value = value

            recipient_data.fields.append(field)

        result = self.client.service.editRecipient(self.login, campaignID,
            recipientID, recipient_data)
        return result

    def flushGroup(self, campaignID, groupID):
        '''
        Flush all recipients from a recipient group, keep the group.
        The recipients are 'disconnected' from the group, not physically deleted.
        Afterwards, the group will still exist, but contains no recipients anymore.
        Required credentials: 'delete' privilege for area 'Groups'
        Returns: Number of recipients actually flushed.
        '''
        raise NotImplementedError

    def getBrands(self):
        '''
        Retrieve all brands from DMdelivery.
        Required credentials: 'export' privilege for area 'Brands'
        Returns: An array of all brands in the DMdelivery environment.
        '''
        result = self.client.service.getBrands(self.login)
        return result

    def getCampaigns(self):
        '''
        Retrieve all campaigns from DMdelivery.
        Required credentials: 'export' privilege for area 'Campaigns'
        Returns: An array of all campaigns in the DMdelivery environment.
        '''
        result = self.client.service.getCampaigns(self.login)
        return result

    def getEventAttendees(self, campaignID, eventID):
        '''
        Get all attendees for an event
        returns: Multidimensional array with recipient data formatted as
        name/value pairs.
        '''
        raise NotImplementedError

    def getEvents(self, campaignID, eventID):
        '''
        Get all events for a specified campaign
        Returns: Complex datatype, All data related to the event.
        '''
        raise NotImplementedError

    def getFilters(self, campaignID,):
        '''
        Get the filters available in a campaign
        Returns: Multidimensional array with filter data containing ID and name
        '''
        raise NotImplementedError

    def getGroups(self, campaignID,):
        '''
        Retrieve all groups from a DMdelivery campaign.
        Required credentials: 'export' privilege for area 'Groups'
        Returns: An array of all groups in the campaign.
        '''
        result = self.client.service.getGroups(self.login, campaignID)
        return result

    def getMailingBounce(self, campaignID, mailingID, types, field, date):
        '''
        Retrieve the response (what recipients opened/clicked) for a mailing.
        Required credentials: access to area 'Statistics'
        Returns: An array containing response info (recipient_id, type
            [hard,soft] and log_date).
        '''
        raise NotImplementedError

    def getMailingResponse(self, campaignID, mailingID, types, field,):
        '''
        Retrieve the response (what recipients opened/clicked) for a mailing.
        Required credentials: access to area 'Statistics'
        Returns: An array containing response info (recipient_id, type
        [open,click,trigger] and log_date).
        '''
        raise NotImplementedError

    def getMailings(self, campaignID, limit, definitiveOnly):
        '''
        Retrieve all mailings from a DMdelivery campaign. Mailings are returned
        from new to old (newest on top).
        Required credentials: 'export' privilege for area 'Mailings'
        Returns: An array of all mailings in the campaign.
        '''
        raise NotImplementedError

    def getMailingStatsSummary(self, campaignID, mailingID,):
        '''
        Retrieve summarized statistics for a mailing sent. Mailing must be
        sent in order to be able to do this. Required credentials: access
        to area 'Statistics'
        Returns: An array containing summary stats info (sent, bounces,
        unsubscribers, opens, clicks, conversion etc).
        '''
        raise NotImplementedError

    def getOverallRecipientCampaigns(self, recipientID):
        '''
        Retrieve all campaigns an overall recipient is member of, and the groups
        they're member of within those campaigns.
        Required credentials: access to area 'Overall recipients'
        Returns: An array of campaigns (and groups) the recipient is member of.
        '''
        raise NotImplementedError

    def getRecipientFields(self, campaignID, lang='es'):
        '''
        campaignID = int

        Retrieve recipient fields for a DMdelivery campaign.
        Required credentials: access to area 'Define fields'
        Returns: An array of all recipient fields defined for the campaign.
        '''
        result = self.client.service.getRecipientFields(self.login,
            campaignID, lang)
        return result

    def getRecipientGroups(self, campaignID, recipientID):
        '''
        Retrieve the groups a recipient is member of.
        Required credentials: 'export' privilege for area 'Groups'
        Returns: An array with all (database IDs of) groups the recipient is
        now a member of.
        '''
        raise NotImplementedError

    def getRecipients(self, campaignID, fields, inGroupIDs, notInGroupIDs,
            mailingIDs, filterID,):
        '''
        Retrieve recipients from a DMdelivery campaign.
        Required credentials: 'export' privilege for area 'Recipients'
        Provide at least one inGroupID or mailingID (inGroupIDs and mailingIDs
        can't both be empty).
        Returns: An array of recipients.
        '''
        raise NotImplementedError

    def getRecipientsByMatch(self, campaignID, recipientMatchData):
        '''
        Retrieve recipients that match certain criteria, including their database ID.
        Required credentials: 'export' privilege for area 'Recipients'
        Returns: An array of recipients that match the criteria.
        '''
        raise NotImplementedError

    def getRecipientsFromGroup(self, campaignID, fields, inGroupID,
            fromDate, mailingIDs, filterID):
        '''
        Retrieve recipients from a specific DMdelivery group.
        Required credentials: 'export' privilege for area 'Recipients'
        Returns:  An array of recipients.
        '''
        raise NotImplementedError

    def getSenderAddresses(self, ):
        '''
        Retrieve all sender addresses from DMdelivery.
        Required credentials: 'export' privilege for area 'Sender addresses'
        Returns: An array of all sender addresses in the DMdelivery environment.
        '''
        raise NotImplementedError

    def getSMSMailings(self, campaignID, limit, definitiveOnly):
        '''
        Retrieve all SMS mailings from a DMdelivery campaign.
        Mailings are returned from new to old (newest on top).
        Required credentials: 'export' privilege for area 'SMS mailings'
        Returns: An array of all SMS maillings in the campaign.
        '''
        raise NotImplementedError

    def importRemoteCSV(self, ):
        '''
        '''
        raise NotImplementedError

    def importRemoteCSVSendMailing(self, ):
        '''
        '''
        raise NotImplementedError

    def moveRecipientsToGroup(self, campaignID, fromGroupID, toGroupID):
        '''
        Move all recipients from one group to another group.
        Required credentials: access to area 'Groups'
        Returns: The number of recipients that were moved to the target group.
        '''
        raise NotImplementedError

    def removeOverallRecipientFromGroups(self, campaignID, recipientID,
            groupIDs):
        '''
        Remove an overall recipient from one or more groups in one or more
        overall campaigns.
        Required credentials: 'delete' privilege for area 'Overall recipients'
        Returns: True.
        '''
        raise NotImplementedError

    def removeRecipientFromGroups(self, campaignID, recipientID, groupIDs):
        '''
        Remove a recipient from one or more groups.
        Required credentials: 'update' privilege for area 'Recipients'
        Returns: An array of groups (database IDs) the recipient is now a member of
        '''
        raise NotImplementedError

    def sendMailing(self, campaignID, mailingID, isTest, resultsEmail,
            groupIDs, filterIDs, langs, ADprefixDomains, excludedGroupIDs,
            callbackUrl=None,):
        '''
        Bulk-send a mailing.
        Required credentials: access to area 'Send mailing'
        Returns: status 'OK'
        '''
        raise NotImplementedError

    def sendMailingScheduled(self, campaignID, mailingID, sendDate,
            isTest, resultsEmail, groupIDs, filterIDs, ADprefixDomains,
            approvalDMDgid, approvalPeriod, approvalAck, approvalNack,
            excludedGroupIDs, callbackUrl=None, ):
        '''
        Bulk-send a mailing at a later date/time, optionally using approval procedure.
        Required credentials: access to area 'Send mailing'
        Returns: status 'OK'
        '''
        raise NotImplementedError

    def sendSingleMail(self, campaignID, mailingID, recipientID,
            attachments, extraRecipientData ):
        '''
        Send a bulk mailing to a single recipient, optionally attaching files.
        The filesize of all attachments is limited to 10MB.
        Required credentials: access to area 'Send mailing'
        Returns: status 'OK'
        '''
        raise NotImplementedError

    def sendSingleMailing(self, campaignID, mailingID, recipientID):
        '''
        Send a mailing to a single recipient. Mainly used for (un)subscribe
        confirmations etc. Of emails sent through this function, no statistics
        will be registered. Do not use this function to send many emails to
        many different recipients! Required credentials: access to area
        'Send mailing'
        Returns: True
        '''
        raise NotImplementedError

    def sendSingleSMS(self, campaignID, mailingID, recipientID):
        '''
        Send an SMS message to a single recipient.
        Required credentials: access to area 'Send SMS mailing'
        Returns: True
        '''
        raise NotImplementedError

    def sendSMS(self, campaignID, mailingID, isTest, resultsEmail,
            groupIDs, filterID, lang, callbackUrl,):
        '''
        Bulk-send an SMS.
        Required credentials: access to area 'Send SMS mailing'
        When messages, after personalizing, exceed a length of 160 characters,
        multiple SMS's are sent.
        Returns: status 'OK'
        '''
        raise NotImplementedError

    def slurpMailing(self, campaignID, mailingName, lang, subject,
            fromName, senderID, url, checkTimeStamp, preheader):
        '''
        Create a mailing from a URL.
        Required credentials: 'insert' privilege for area 'Mailings'
        Returns: The database ID of the mailing that was created.
        '''
        raise NotImplementedError