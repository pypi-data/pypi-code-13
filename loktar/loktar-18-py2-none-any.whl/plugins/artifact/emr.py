from loktar.cmd import exe
from loktar.exceptions import CIBuildPackageFail
from loktar.plugin import SimplePlugin
from loktar.store import store_artifact


def run(*args, **kwargs):
    """This is a wrapper for running the plugin

    """
    try:
        Jar(*args).run()
    except IndexError:
        print(Jar.__init__.__doc__)
        raise


# Maybe this plugin is a maven plugin I don' know ....

class EMR():
    pass


class Jar(SimplePlugin):
        def __init__(self, package_info, remote):
            """Plugin for building jar package

                Args:
                    package_info (dict): Contains information about the package to execute inside the plugin
                    remote (bool): Define if the plugin will be execute in remote or not

                Raises:
                    CIBuildPackageFail: when one of the steps for packaging or uploading the package failed
            """
            SimplePlugin.__init__(self, package_info,
                                  {
                                      "command": {
                                          "run": None,
                                          "clean": "make clean"
                                      }
                                  },
                                  remote=remote)
            self.timeline = {
                10: self.get_next_version,
                20: self.release,
                40: self.store

            }

        def run(self):
            """Default method for running the timeline

            """
            self._run()

        def get_next_version(self):
            """Get the next version for the current package

            """
            if self.package_info["mode"] == "master":
                try:
                    pass
                except IndexError:
                    self.share_memory["latest_version"] = 1
            else:
                self.share_memory["latest_version"] = self.package_info["mode"]

        def release(self):
            """Create the package

            """
            with self.cwd(self.path):
                if not exe(zip_command, remote=self.remote):
                    raise CIBuildPackageFail("the command : {} executed in the directory {} return False"
                                             .format(zip_command))

        def upload(self):
            """Upload the package previously build


            """
            if self.package_info["build_info"]["artifact_storage"] == "nexus":
                pass
            elif self.package_info["build_info"]["artifact_storage"] == "artifactory":
                pass
            else:
                try:
                    store_artifact(self.package_info["build_info"]["artifact_storage"], )
                except Exception as e:
                    error_msg = str(e)
                    self.logger.error(error_msg)
                    raise CIBuildPackageFail(error_msg)
