
import os

from zope.component import getGlobalSiteManager
from zope.component import getUtility
from zope.interface import implements
from zope.interface import Interface
import boto3
import json
from prettyprint import pp

from interfaces import IFWUtils

gsm = getGlobalSiteManager()


class Boto3Session(object):
    implements(IFWUtils)
    def __init__(self):
        self.aws_profile = os.environ.get('AWS_PROFILE')
        self.session = boto3.Session(profile_name=self.aws_profile)
    def __call__(self):
        return self.session
boto3_session = Boto3Session()
gsm.registerUtility(boto3_session, IFWUtils, 'boto3_session')


class Boto3IAMConnection(object):
    implements(IFWUtils)
    def __init__(self):
        pass
        #s = boto3.Session()
        #services = s.get_available_services()
    def __call__(self):
        try:
            return getUtility(IFWUtils,'boto3_session').client('iam')
        except AttributeError:
            print "no valid boto3.session object exists"
            return None
boto3_iam_conn = Boto3IAMConnection()
gsm.registerUtility(boto3_iam_conn, IFWUtils, 'boto3_iam_conn')

