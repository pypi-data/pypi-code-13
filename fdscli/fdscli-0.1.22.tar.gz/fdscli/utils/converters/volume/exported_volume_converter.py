#
# Copyright 2016 Formation Data Systems, Inc. All Rights Reserved.
#
import json
from model.volume.exported_volume import ExportedVolume

class ExportedVolumeConverter(object):
    '''Helper class for marshalling between ExportedVolume and JSON formatted string.

    The term 'to marshal' means to convert some data from internal to external form
    (in an RPC buffer for instance). The term 'unmarshalling' refers to the reverse
    process. We presume that the server will use reflection to create a Java object
    given the JSON formatted string.
    '''

    @staticmethod
    def to_json(exported_volume):
        '''
        Converts an ExportedVolume object into JSON format.
        We presume that the recipient (a server) uses a package like Gson and passes the type
        literal when deserializing the JSON formatted string.

        Parameters
        ----------
        exported_volume (ExportedVolume): Metadata for a volume exported to a bucket.

        Returns
        -------
        str : JSON formatted string
        '''
        d = dict()

        d["objectPrefixKey"] = exported_volume.obj_prefix_key
        d["originalVolumeName"] = exported_volume.source_volume_name
        d["volumeType"] = exported_volume.source_volume_type
        d["creationTime"] = str(exported_volume.creation_time)
        d["blobCount"] = str(exported_volume.blob_count)

        result = json.dumps(d)
        return result;

    @staticmethod
    def build_exported_volume_from_json(j_exported_volume):
        '''
        Converts dictionary or JSON formatted string into an ExportedVolume object.

        Parameters
        ----------
        j_exported_volume (str | dict)

        Returns
        -------
        ExportedVolume
        '''
        exported_volume = ExportedVolume()

        if not isinstance(j_exported_volume, dict):
            j_exported_volume = json.loads(j_exported_volume)

        exported_volume.obj_prefix_key = j_exported_volume.pop( "objectPrefixKey", 
            exported_volume.obj_prefix_key)
        exported_volume.source_volume_name = j_exported_volume.pop( "originalVolumeName", 
            exported_volume.source_volume_name)
        exported_volume.source_volume_type = j_exported_volume.pop( "volumeType", 
            exported_volume.source_volume_type)
        exported_volume.creation_time = long(j_exported_volume.pop( "creationTime", 
            exported_volume.creation_time))
        exported_volume.blob_count = int(j_exported_volume.pop( "blobCount", 
            exported_volume.blob_count))

        return exported_volume

