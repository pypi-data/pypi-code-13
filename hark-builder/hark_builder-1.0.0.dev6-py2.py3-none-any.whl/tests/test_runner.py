import os
import unittest

import hark_builder.build
from hark_builder.exceptions import BuildFailed, NoArtifact
import hark_builder.runner

from .util import patch, MagicMock

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


class TestBuildRunner(unittest.TestCase):

    @patch('os.listdir')
    def test_artifact_filename(self, mockListDir):
        # test when there's been a build
        ret = [
            'packer-Debian-7_virtualbox-1468832493-disk1.vmdk',
            'packer-Debian-7_virtualbox-1468832493.ovf'
        ]
        mockListDir.return_value = ret

        b = hark_builder.build.Build.by_name('Debian-8_virtualbox')
        image_cache = MagicMock()
        runner = hark_builder.runner.BuildRunner(
            b, image_cache, '/blah', 1)

        assert runner.artifact_filename() == os.path.join(
            '/blah',
            'output-Debian-8_virtualbox',
            ret[0])

        # test when no build has been run
        mockListDir.side_effect = FileNotFoundError
        self.assertRaises(
            NoArtifact, runner.artifact_filename)

        # test when there is an empty dir
        mockListDir.side_effect = None
        mockListDir.return_value = []
        self.assertRaises(
            NoArtifact, runner.artifact_filename)

    @patch('hark.lib.command.TerminalCommand')
    def test_run_build(self, mockCommand):
        b = hark_builder.build.Build.by_name('Debian-8_virtualbox')

        mockCommandImpl = mockCommand.return_value
        mockCommandImpl.run.return_value = 0

        image_cache = MagicMock()
        fbip = image_cache.full_base_image_path
        fbip.return_value = 'https://example.com/'

        working_dir = '/blah'

        runner = hark_builder.runner.BuildRunner(
            b, image_cache, working_dir, 1)

        runner.run_build()

        file_path = hark_builder.build.packer_file_path()

        expectCmd = [
            'packer',
            'build',
            '-only=Debian-8_virtualbox',
            '-var', 'output_dir=/blah',
            '-var', 'iso_url=https://example.com/',
            file_path,
        ]
        expectEnv = {
            'PACKER_CACHE_DIR': os.path.join(working_dir, 'packer_cache')
        }

        mockCommand.assert_called_with(
            expectCmd, cwd=os.path.dirname(file_path), env=expectEnv)

        # test with force=True
        eC = list(expectCmd)
        eC.insert(len(eC)-1, '-force')
        runner.run_build(force=True)
        mockCommand.assert_called_with(
            eC, cwd=os.path.dirname(file_path), env=expectEnv)

        # test with failed command
        mockCommandImpl.run.return_value = 1
        self.assertRaises(BuildFailed, runner.run_build)

    @patch('os.path.exists')
    @patch('hark_builder.runner.BuildRunner.artifact_filename')
    def test_build_artifact_exists(self, mockArtifactFilename, mockPathExists):
        runner = hark_builder.runner.BuildRunner(
            MagicMock(), MagicMock(), MagicMock(), 1)

        mockArtifactFilename.return_value = ''
        mockPathExists.return_value = False
        assert not runner.build_artifact_exists()

        mockArtifactFilename.return_value = ''
        mockPathExists.return_value = True
        assert runner.build_artifact_exists()

        mockArtifactFilename.side_effect = NoArtifact
        mockPathExists.return_value = False
        assert not runner.build_artifact_exists()

    @patch('os.stat')
    @patch('hark_builder.runner.BuildRunner.artifact_filename')
    def test_build_artifact_info(self, mockArtifactFilename, mockStat):
        runner = hark_builder.runner.BuildRunner(
            MagicMock(), MagicMock(), MagicMock(), 1)

        mockArtifactFilename.return_value = 'blah'

        class FakeStat(object):
            st_size = 1073741824

        mockStat.return_value = FakeStat

        assert runner.build_artifact_info() == {
            'filename': 'blah',
            'size_mb': 1024,
        }

    @patch('hark_builder.runner.BuildRunner.artifact_filename')
    def test_upload_build_artifact(self, mockArtifactFilename):
        runner = hark_builder.runner.BuildRunner(
            MagicMock(), MagicMock(), MagicMock(), 1)

        mockArtifactFilename.return_value = '/dev/null'

        runner.upload_build_artifact()
