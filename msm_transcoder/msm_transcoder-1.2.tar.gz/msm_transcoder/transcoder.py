
import json

class Transcoder( object ):

    def __hex( self, number ):

        return hex( number ).replace( "0x", "" )

    def __encodeNum( self, num, data, maxBytes ):

        result = self.__hex( num )
        zeroNum = ( maxBytes * 2 ) - len( result )

        for i in range( zeroNum ):

            result = "0" + result

        for i in range( len( result ) ):

            index = i * 2

            if index >= len( result ):

                break

            data.append( int( result[index:index+2] , 16 ) )

    def __decodeNum( self, data, beginIndex, numBytes ):

        result = ""

        for i in range( numBytes ):

            numStr = self.__hex( data[beginIndex + i] )

            if len( numStr ) == 1:

                numStr = "0"+numStr

            result += numStr

        return int( result , 16 )

    def __encodeBoolean( self, value, data ):

        if value:

            data.append( 49 )

        else:

            data.append( 48 )

    def __decodeBoolean( self, data, index ):

        return data[index] == 49

    def __encodeString( self, string ):

        data = list(map( ord, string ))

        return {"length": len(data),"data":data}

    def __decodeString( self, data, beginIndex, length ):

        #result = [0] * ( length - beginIndex ) + data[beginIndex:beginIndex+length]
        result = data[beginIndex:beginIndex+length]
        return ''.join( map( chr, result ) )
        #return ''.join( map( chr, data ) )

    def __pushAll( self, arr1, arr2 ):

        for i in arr2:

            arr1.append( i )

    def serialize( self, sessionObj ):

        bytes_ = []

        self.__encodeNum( sessionObj.get( "version" ), bytes_, 2 )
        self.__encodeNum( sessionObj.get( "sessionFieldsDataLength") , bytes_, 2 )
        self.__encodeNum( sessionObj.get( "creationTime" ) , bytes_, 8 )
        self.__encodeNum( sessionObj.get( "lastAccessedTime" ) , bytes_, 8 )
        self.__encodeNum( sessionObj.get( "maxInactive" ) , bytes_, 4 )
        self.__encodeBoolean( sessionObj.get( "isNew" ), bytes_ )
        self.__encodeBoolean( sessionObj.get( "isValid" ), bytes_ )
        self.__encodeNum( sessionObj.get( "thisAccessedTime" ), bytes_, 8 )
        self.__encodeNum( sessionObj.get( "lastBackupTime" ), bytes_, 8 )

        idResult = self.__encodeString( sessionObj.get( "id" ) )
        #print "id length {0}".format( len( idResult ) )
        self.__encodeNum(  idResult.get( "length" ), bytes_, 2 )
        self.__pushAll( bytes_, idResult.get( "data" ) )

        self.__encodeNum( sessionObj.get( "authType" ), bytes_, 2 )

        principalDataResult = self.__encodeString( json.dumps( sessionObj.get( "principalData"), ensure_ascii = False ) )

        principalDataResult["length"] = 0

        self.__encodeNum( principalDataResult.get( "length" ), bytes_, 2 )

        if principalDataResult.get( "length" ) == 0:

            self.__encodeNum( 0, bytes_, 2 )
            self.__encodeNum( 0, bytes_, 2 )
            self.__pushAll( bytes_, principalDataResult.get( "data" ) )

        else:

            self.__pushAll( bytes_, principalDataResult.get( "data" ) )

            savedRequestDataResult = self.__encodeString( json.dumps( sessionObj.get( "savedRequestData" ), ensure_ascii = False ) )
            self.__encodeNum( savedRequestDataResult.get( "length" ), bytes_, 2 )
            self.__pushAll( bytes_, savedRequestDataResult.get( "data" ) )

            savedPrincipalDataResult = self.__encodeString( json.dumps( sessionObj.get( "savedPrincipalDataResult" ), ensure_ascii = False ) )
            self.__encodeNum( savedPrincipalDataResult.get( "length" ), bytes_, 2 )
            self.__pushAll( bytes_, savedPrincipalDataResult.get( "data" ) )
    
        return bytes_

    def deserialize( self, dataBytes ):

        result = dict()
        result["version"] = self.__decodeNum( dataBytes, 0 , 2 )
        result["sessionFieldsDataLength"] = self.__decodeNum( dataBytes, 2, 2 )
        result["creationTime"] = self.__decodeNum( dataBytes, 4, 8 )
        result["lastAccessedTime"] = self.__decodeNum( dataBytes, 12, 8 )
        result["maxInactive"] = self.__decodeNum( dataBytes, 20, 4 )
        result["isNew"] = self.__decodeBoolean( dataBytes, 24 )
        result["isValid"] = self.__decodeBoolean( dataBytes, 25 )
        result["thisAccessedTime"] = self.__decodeNum( dataBytes, 26, 8 )
        result["lastBackupTime"] = self.__decodeNum( dataBytes, 34, 8 )
        result["idLength"] = self.__decodeNum( dataBytes, 42, 2 )
        result["id"] = self.__decodeString( dataBytes, 44, result.get( "idLength" ) )
        result["authType"] = self.__decodeNum( dataBytes, 44 + result.get( "idLength" ), 2 )

        result["principalDataLength"] = self.__decodeNum( dataBytes, 46 + result.get( "idLength" ), 2 )

        if result.get( "principalDataLength" ) == 0:

            #print  self.__decodeString( dataBytes, result.get( "sessionFieldsDataLength" ), len( dataBytes ) - result.get( "sessionFieldsDataLength" ) )
            #import pdb;pdb.set_trace()
            result["principalData"] = json.loads( self.__decodeString( dataBytes, result.get( "sessionFieldsDataLength" ), len( dataBytes ) - result.get( "sessionFieldsDataLength" ) ) )

        else:
            result["principalData"] = json.loads( self.__decodeString( dataBytes, 48 + result.get( "idLength" ) , result.get( "principalDataLength" ) ) )

        result["savedRequestDataLength"] = self.__decodeNum( dataBytes, 48 + result.get( "idLength" ) + result.get("principalDataLength"), 2 )

        if result.get( "savedRequestDataLength" ) != 0:

            result["savedRequestData"] = json.loads( self.__decodeString( dataBytes, 50 + result.get( "idLength" ) + result.get( "principalDataLength" ) , result.get( "savedRequestDataLength" ) ) )


        result["savedPrincipalDataLength"] = self.__decodeNum( dataBytes, 50 + result.get( "idLength" ) + result.get("principalDataLength") + result.get( "savedRequestDataLength" ), 2 )

        if result.get( "savedPrincipalDataLength" ) != 0:

            result["savedPrincipalData"] = json.loads( self.__decodeString( dataBytes, 52 + result.get( "idLength" ) + result.get( "principalDataLength" ) + result.get( "savedRequestDataLength" ), result.get( "savedPrincipalDataLength" ) ) )

        return result



