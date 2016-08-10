import os

from ievv_opensource.utils.ievvbuildstatic import pluginbase
from ievv_opensource.utils.ievvbuildstatic.installers.npm import NpmInstaller
from ievv_opensource.utils.shellcommandmixin import ShellCommandMixin, ShellCommandError


class Plugin(pluginbase.Plugin, ShellCommandMixin):
    """
    SASS build plugin --- builds .scss files into css, and supports watching
    for changes.

    By default, we assume ``sassc`` is available on PATH, but you can
    override the path to the sassc executable by setting the
    ``IEVVTASKS_BUILDSTATIC_SASSC_EXECUTABLE`` environment variable.

    Examples:

        Very simple example where the source file is in
        ``demoapp/staticsources/styles/theme.scss``::

            IEVVTASKS_BUILDSTATIC_APPS = ievvbuildstatic.config.Apps(
                ievvbuildstatic.config.App(
                    appname='demoapp',
                    version='1.0.0',
                    plugins=[
                        ievvbuildstatic.sassbuild.Plugin(sourcefile='theme.scss'),
                    ]
                )
            )

        A more complex example that builds a django-cradmin theme
        where sources are split in multiple directories, and
        the bower install directory is on the scss path
        (the example also uses :class:`ievv_opensource.utils.ievvbuildstatic.bowerinstall.Plugin`)::

            IEVVTASKS_BUILDSTATIC_APPS = ievvbuildstatic.config.Apps(
                ievvbuildstatic.config.App(
                    appname='demoapp',
                    version='1.0.0',
                    plugins=[
                        ievvbuildstatic.bowerinstall.Plugin(
                            packages={
                                'bootstrap': '~3.1.1'
                            }
                        ),
                        ievvbuildstatic.sassbuild.Plugin(
                            sourcefolder='styles/cradmin_theme_demoapp',
                            sourcefile='theme.scss',
                            other_sourcefolders=[
                                'styles/cradmin_base',
                                'styles/cradmin_theme_default',
                            ],
                            sass_include_paths=[
                                'bower_components',
                            ]
                        )
                    ]
                )
            )
    """

    name = 'sassbuild'

    def __init__(self, sourcefile, sourcefolder='styles',
                 other_sourcefolders=None,
                 sass_include_paths=None):
        """
        Parameters:
            sourcefile: Main source file (the one including all other scss files)
                relative to ``sourcefolder``.
            sourcefolder: The folder where ``sourcefile`` is located relative to
                the source folder of the :class:`~ievv_opensource.utils.ievvbuild.config.App`.
            sass_include_paths: Less include paths as a list. Paths are relative
                to the source folder of the :class:`~ievv_opensource.utils.ievvbuild.config.App`.

        """
        self.sourcefolder = sourcefolder
        self.other_sourcefolders = other_sourcefolders
        self.sass_include_paths = sass_include_paths
        self.sourcefile = os.path.join(sourcefolder, sourcefile)

    def get_sourcefile_path(self):
        return self.app.get_source_path(self.sourcefile)

    def get_destinationfile_path(self):
        return self.app.get_destination_path(
            self.sourcefile, new_extension='.css')

    def get_other_sourcefolders_paths(self):
        return map(self.app.get_source_path, self.other_sourcefolders)

    def format_sass_include_paths(self):
        if self.sass_include_paths:
            return ':'.join(map(self.app.get_source_path, self.sass_include_paths))
        else:
            return ''

    def get_sassc_executable(self):
        return os.environ.get('IEVVTASKS_BUILDSTATIC_SASSC_EXECUTABLE', 'sassc')

    def run(self):
        self.get_logger().command_start('Building {source} into {destination}.'.format(
            source=self.get_sourcefile_path(),
            destination=self.get_destinationfile_path()))

        destinationdirectory = os.path.dirname(self.get_destinationfile_path())
        if not os.path.exists(destinationdirectory):
            os.makedirs(destinationdirectory)

        executable = self.get_sassc_executable()
        kwargs = {}
        sass_include_paths = self.format_sass_include_paths()
        if sass_include_paths:
            kwargs['load_path'] = sass_include_paths
            self.get_logger().info('Using --load-path={}'.format(sass_include_paths))
        try:
            self.run_shell_command(executable,
                                   args=[
                                       self.get_sourcefile_path(),
                                       self.get_destinationfile_path()
                                   ],
                                   kwargs=kwargs)
        except ShellCommandError:
            self.get_logger().command_error('SASS build FAILED!')
        else:
            self.get_logger().command_success('SASS build successful :)')

    def get_watch_folders(self):
        """
        We only watch the folder where the scss sources are located,
        so this returns the absolute path of the ``sourcefolder``.
        """
        folders = [self.app.get_source_path(self.sourcefolder)]
        if self.other_sourcefolders:
            folders.extend(self.get_other_sourcefolders_paths())
        return folders

    def get_watch_regexes(self):
        return ['^.+[.]sass$']

    def __str__(self):
        return '{}({})'.format(super(Plugin, self).__str__(), self.sourcefile)
