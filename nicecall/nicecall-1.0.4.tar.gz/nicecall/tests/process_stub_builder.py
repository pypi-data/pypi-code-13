import nicecall


class ProcessStubBuilder():
    def __init__(self):
        self._matches = {}

    def add_match(self, args, exitcode, stdout=[], stderr=[]):
        key = self._generate_key(args)
        self._matches[key] = (exitcode, stdout, stderr)

    def build(self):
        matches = self._matches

        class ProcessStub(nicecall.Process):
            def execute(stub):
                key = self._generate_key(stub.args)
                exitcode, stdout, stderr = matches[key]

                for line in stdout:
                    for action in stub._on_stdout:
                        action(line)

                for line in stderr:
                    for action in stub._on_stderr:
                        action(line)

                return exitcode

        return ProcessStub

    def _generate_key(self, args):
        parts = [a.replace("\\", "\\\\").replace(",", "\\,") for a in args]
        return ",".join(parts)
