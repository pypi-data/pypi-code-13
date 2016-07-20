#
# Copyright 2016 Formation Data Systems, Inc. All Rights Reserved.
#
from base_cli_test import BaseCliTest
from mock import patch
import mock_functions
from model.volume.volume import Volume
from utils.converters.volume.volume_converter import VolumeConverter

class VolumeImportTest( BaseCliTest ):
    '''
    Test case for volume import. IS-A unittest.TestCase.
    '''
    @patch("plugins.volume_plugin.VolumePlugin.pretty_print_volume", side_effect=mock_functions.empty_one)
    @patch("services.response_writer.ResponseWriter.writeTabularData", side_effect=mock_functions.empty_one)
    @patch("services.volume_service.VolumeService.import_volume", side_effect=mock_functions.importVolume)
    def test_import_volume(self, mockImportVolume, mockTabular, mockPretty):
        '''
        The volume service calls are replaced by mock functions.

        Parameters
        ----------
        mockImportVolume (unittest.mock.MagicMock)
        mockTabular (unittest.mock.MagicMock)
        mockPretty (unittest.mock.MagicMock)
        '''
        args = ["volume", "import", "-name=newvol", "-s3_object_prefix=1/42/2016-04-04T00:00:01", 
            "-s3_bucket_name=xvolrepo", "-s3_access_key=ABCDEFG",
            "-s3_secret_key=/52/yrwhere", "-url=https://s3.amazon.com"]

        self.callMessageFormatter(args)
        self.cli.run(args)
        assert mockImportVolume.call_count == 1

        volume_name = mockImportVolume.call_args[0][0]

        assert volume_name == "newvol"

        repo = mockImportVolume.call_args[0][1]

        assert repo.url == "https://s3.amazon.com"
        assert repo.bucket_name == "xvolrepo"
        assert repo.remote_om == None
        assert repo.obj_prefix_key == "1/42/2016-04-04T00:00:01"
        assert repo.credentials.access_key_id == "ABCDEFG"
        assert repo.credentials.secret_key == "/52/yrwhere"

        print("test_import_volume passed.\n\n")

