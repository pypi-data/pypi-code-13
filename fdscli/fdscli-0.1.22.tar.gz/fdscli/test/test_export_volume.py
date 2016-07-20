#
# Copyright 2016 Formation Data Systems, Inc. All Rights Reserved.
#
from base_cli_test import BaseCliTest
from mock import patch
import mock_functions
from model.volume.volume import Volume
from utils.converters.common.repository_converter import RepositoryConverter
from utils.converters.volume.volume_converter import VolumeConverter

class VolumeExportTest( BaseCliTest ):
    '''
    Test case for volume export. IS-A unittest.TestCase.
    '''
    @patch("plugins.volume_plugin.VolumePlugin.pretty_print_volume", side_effect=mock_functions.empty_one)
    @patch("services.response_writer.ResponseWriter.writeTabularData", side_effect=mock_functions.empty_one)
    @patch("services.volume_service.VolumeService.export_volume", side_effect=mock_functions.exportVolume)
    @patch("services.volume_service.VolumeService.get_volume", side_effect=mock_functions.getVolume)
    def test_export_volume(self, mockGetVolume, mockExportVolume, mockTabular, mockPretty):
        '''
        The volume service calls are replaced by mock functions.

        Parameters
        ----------
        mockGetVolume (unittest.mock.MagicMock)
        mockExportVolume (unittest.mock.MagicMock)
        mockTabular (unittest.mock.MagicMock)
        mockPretty (unittest.mock.MagicMock)
        '''
        args = ["volume", "export", "-volume_id=3", "-s3_bucket_name=xvolrepo", "-s3_access_key=ABCDEFG",
            "-s3_secret_key=/52/yrwhere", "-url=https://s3.amazon.com"]

        self.callMessageFormatter(args)
        self.cli.run(args)
        assert mockExportVolume.call_count == 1

        volume = mockExportVolume.call_args[0][0]

        assert volume.id == 3

        repo = mockExportVolume.call_args[0][1]

        j_repo = RepositoryConverter.to_json(repo)
        print j_repo

        assert repo.url == "https://s3.amazon.com"
        assert repo.bucket_name == "xvolrepo"
        assert repo.remote_om == None
        assert repo.credentials.access_key_id == "ABCDEFG"
        assert repo.credentials.secret_key == "/52/yrwhere"

        print("test_export_volume passed.\n\n")

    @patch("plugins.volume_plugin.VolumePlugin.pretty_print_volume", side_effect=mock_functions.empty_one)
    @patch("services.response_writer.ResponseWriter.writeTabularData", side_effect=mock_functions.empty_one)
    @patch("services.volume_service.VolumeService.export_volume", side_effect=mock_functions.exportVolume)
    @patch("services.volume_service.VolumeService.get_volume", side_effect=mock_functions.getVolume)
    def test_export_volume_error(self, mockGetVolume, mockExportVolume, mockTabular, mockPretty):
        '''
        The volume service calls are replaced by mock functions.

        Parameters
        ----------
        mockGetVolume (unittest.mock.MagicMock)
        mockExportVolume (unittest.mock.MagicMock)
        mockTabular (unittest.mock.MagicMock)
        mockPretty (unittest.mock.MagicMock)
        '''
        args = ["volume", "export", "-volume_id=1", "-s3_bucket_name=xvolrepo", "-s3_access_key=ABCDEFG",
            "-s3_secret_key=/52/yrwhere", "-url=https://s3.amazon.com"]

        self.callMessageFormatter(args)

        print("Testing no volume")

        try:
            self.cli.run(args)
        except SystemExit as se:
            exception = se

        assert exception != None, "Expected to get an exception but got none"

        assert mockExportVolume.call_count == 0

