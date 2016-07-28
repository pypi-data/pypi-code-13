
import base64
import pylibmc
from msm_transcoder import Transcoder
import time
import uuid
import sys

class MemorySessionAPI( object ):

    def __init__( self, hosts = ["127.0.0.1"] ):

        self.__hosts = hosts
        self.__mc = pylibmc.Client( hosts,  binary=True )
        self.__transcoder = Transcoder()

    def create_session_data( self ):

        creationTime = int ( time.time() * 1000 )

        session_data = dict()
        session_data["version"] = 2
        session_data["sessionFieldsDataLength"] = 84
        session_data["creationTime"] = creationTime
        session_data["lastAccessedTime"] = creationTime
        session_data["maxInactive"] = 7200
        session_data["isNew"] = True
        session_data["isValid"] = True
        session_data["thisAccessedTime"] = creationTime
        session_data["lastBackupTime"] = creationTime
        session_data["id"] = uuid.uuid1().hex
        session_data["idLength"] = len( session_data["id"] )
        session_data["authType"] = 0
        session_data["principalDataLength"] = 0
        session_data["savedRequestDataLength"] = 0
        session_data['principalData'] = {}

        return session_data

    def get_data( self, session_id ):

        b64_session = self.__mc.get( session_id )

        if b64_session:

            bin_session = base64.b64decode( b64_session )

            if sys.version_info[0] > 2: bin_session = bin_session.decode('iso-8859-1')

            buffers = list( map( ord, bin_session ))

            data = self.__transcoder.deserialize( buffers )


        else:

            data = self.create_session_data()

            #bin_data = ''.join( map( chr, self.__transcoder.serialize( data ) ) ) 

            #output = base64.b64encode( bin_data )

        return data

    def get_user_data( self, session_id ):

        data = self.get_data( session_id )

        return data.get( "principalData" )

    def update_user_data( self, session_id, user_data ):

         data = self.get_data( session_id )

         data["principalData"] = user_data

         bin_data = ''.join( map( chr, self.__transcoder.serialize( data ) ) )

         if sys.version_info[0] > 2: bin_data = bin_data.encode('iso-8859-1')

         output = base64.b64encode( bin_data )

         self.__mc.set( session_id , output)

    def has_login( self, session_id ):

        principalData = self.get_user_data( session_id )

        if principalData.get( "logined" ) is True:

            return True

        else:

            return False

    

