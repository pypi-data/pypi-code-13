from subprocess import check_output as os_check_output
from subprocess import CalledProcessError
"""Instruction sets are dicts, and IDs/synonyms are string-pointers."""
instructions = {
    # Arch Linux
    'arch': {
        'install': 'sudo pacman -S {packages}'
    },
    'ManjaroLinux': 'arch'
}


class Shell:

    def __init__(self):
        pass

    @classmethod
    def check_output(cls, instruction):
        """Utility interface of `subprocess.check_output`.

        Will sanatize output by attempting to decode the data to 'utf-8' format,
        strip all strings, and will not return empty-strings in a list.

        Type-marshalling, validation, etc. are the responsibility of the user.

        Args:
            instruction (str, list): `subprocess.check_output` takes either a
                string or joinable-list as input.

        Returns:
            output (str, list): Attempts to return a string, but returns a list
                of strings if multiple have been found.

        """

        try:
            output = os_check_output(
                instruction, shell=True).decode('utf-8').split('\n')

            # Sanatized returns:
            if type(output) is str:
                return output.strip()

            output.remove('')
            if output.__len__() == 1:
                return output[0].strip()

            return [s.strip() for s in output]
        except CalledProcessError:
            return False

    @classmethod
    def os_id(cls):
        try:
            r = check_output('lsb_release -id', shell=True)
            title = r.decode('utf-8').split('\n') \
                        [0].replace('Distributor ID:', '').strip()
        except:
            pass

        # TODO: test.
        if not title:
            try:
                r = check_output('uname -r', shell=True)
                title = r.decode('utf-8').split('-')[-1]
            except:
                pass

        return title
