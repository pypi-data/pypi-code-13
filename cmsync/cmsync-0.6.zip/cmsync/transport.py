#! /usr/bin/python3
import os
import stat
import shutil

from .color import Color


class Transport:
    """
    """

    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

        self.valid = None

    def is_valid(self):
        """
        """
        if not os.path.exists(self.src):
            print(
                Color.ERROR + "Error: Path not found: '{}'.".format(self.src)
            )
            return False

        return True

    def _remove_readonly(self, func, path, _):
        """
        """
        print('')
        print("Clearing readonly bit and reattempt removal of '{}'".format(path))
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def send(self):
        """
        """
        if self.valid is None:
            if not self.is_valid():
                return False

        self.send_local()
            

    def send_local(self):

        # If source and destination are files
        if os.path.isfile(self.src) and os.path.isfile(self.dest):
            print(
                Color.WARNING +
                "Deleting file '{}'... ".format(self.dest), end=''
            )
            os.remove(self.dest)
            print('Done.')

        # if source is a file and destination is not a file
        elif os.path.isfile(self.src) and not os.path.isfile(self.dest):
            if not os.path.isdir(self.dest):
                print(
                    Color.WARNING +
                    "Creating folder '{}'... ".format(self.dest), end=''
                )
                os.makedirs(self.dest)
                print('Done.')

        # if source and destination are folders
        elif os.path.isdir(self.src) and os.path.isdir(self.dest):
            print(
                Color.WARNING +
                "Deleting folder '{}'... ".format(self.dest),
                end=''
            )
            shutil.rmtree(self.dest, onerror=self._remove_readonly)
            print('Done.')

        print('')

        # copying files
        print(Color.INFO + "Source:      '{}'".format(self.src))
        print(Color.INFO + "Destination: '{}'".format(self.dest))

        if os.path.isfile(self.src):
            print(Color.INFO + "Copying file... ", end='')
            shutil.copy(self.src, self.dest)
            print('Done.')
        else:
            print(Color.INFO + "Copying files... ", end='')
            shutil.copytree(self.src, self.dest)
            print('Done.')