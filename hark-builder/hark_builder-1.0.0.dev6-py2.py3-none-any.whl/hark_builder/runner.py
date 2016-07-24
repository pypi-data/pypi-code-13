import os

import hark.models.base_image
import hark.models.image
import hark.lib.command

import hark_builder.build
from hark_builder.exceptions import BuildFailed, NoArtifact

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


class BuildRunner(object):
    """
    Class to run a build.
    """

    def __init__(self, build, image_cache, working_dir, image_version):
        """
        image_cache should be an S3ImageCache.
        """
        self.build = build
        self.image_cache = image_cache
        self.working_dir = working_dir
        self.image_version = image_version
        self.target_image = hark.models.image.Image(
            driver=self.build.driver,
            guest=self.build.guest,
            version=self.image_version)

    def artifact_filename(self):
        try:
            d = os.path.join(
                self.working_dir,
                'output-%s_%s' % (self.build.guest, self.build.driver))

            for f in os.listdir(d):
                if f.endswith(self.target_image.file_suffix()):
                    return os.path.join(d, f)
        except FileNotFoundError:
            pass

        raise NoArtifact()

    def run_build(self, force=False):
        file_path = hark_builder.build.packer_file_path()

        packer_cache_path = os.path.join(self.working_dir, 'packer_cache')

        # FIXME(cera) - Do not hard code version 1 here.
        #
        # Maybe see what versions are available by listing the bucket?
        base_image = hark.models.base_image.BaseImage(
            guest=self.build.guest, version=1)

        iso_url = self.image_cache.full_base_image_path(base_image)

        cmd = [
            'packer',
            'build',
            '-only=' + self.build.name,
            '-var', 'output_dir=' + self.working_dir,
            '-var', 'iso_url=' + iso_url,
        ]

        if force:
            cmd.append('-force')

        cmd.append(file_path)

        cwd = os.path.dirname(file_path)

        env = {
            'PACKER_CACHE_DIR': packer_cache_path
        }

        cmd = hark.lib.command.TerminalCommand(cmd, cwd=cwd, env=env)

        ret = cmd.run()
        if ret != 0:
            raise BuildFailed('packer exited with exit status %d' % ret)

    def build_artifact_exists(self):
        try:
            return os.path.exists(self.artifact_filename())
        except NoArtifact:
            return False

    def build_artifact_size(self):
        st = os.stat(self.artifact_filename())
        return st.st_size

    def build_artifact_info(self):
        """
        Return a dictionary with stats about the build artifact.
        """
        fname = self.artifact_filename()
        size = self.build_artifact_size()
        return {
            'filename': fname,
            'size_mb': (size >> 20)
        }

    def upload_build_artifact(self, callback=None):
        self.image_cache.upload_image(
            self.target_image, self.artifact_filename(), callback=callback)
