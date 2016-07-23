# vi:et:ts=4 sw=4 sts=4

import fnmatch
import os
import subprocess
import tempfile


class Pipeline(object):
    def __init__(self, config, path, branch):
        self.config = config
        self.build_path = os.path.abspath(path)
        self.branch = branch

        self.steps = self._get_steps()

    def _get_steps(self):
        if "branches" in self.config["pipelines"]:
            for pattern, steps in self.config["pipelines"]["branches"].iteritems():
                if fnmatch.fnmatch(self.branch, pattern):
                    return steps

        return self.config["pipelines"]["default"]


    def _determine_image(self, step):
        return step.get("image", self.config.get("image"))

    def _build_script(self, step):
        fd, filename = tempfile.mkstemp(prefix='pipeline', suffix='.sh')

        with os.fdopen(fd, "w") as ofp:
            content = " && \\\n".join(step["script"])
            ofp.write(content)

        return filename

    def get_command(self, step):
        cmd = [
            "docker",
            "run",
            "--rm=true",
            # TODO cid
            "--entrypoint=/bin/bash",
            "--memory=2048m",
            # TODO envfile
            "-v {script_filename}:/tmp/{script_filename}:ro",
            "-v {build_path}:/opt/atlassian/bitbucketci/agent/build:rw",
            "-w /opt/atlassian/bitbucketci/agent/build",
            "--label com.atlassian.pipelines.agent=\"local\"",
            "{image}",
            # TODO didn't work for me... "-i",
            "/tmp/{script_filename}",
        ]

        return " ".join(cmd).format(
            script_filename=self._build_script(step),
            build_path=self.build_path,
            image=self._determine_image(step),
        )

    def _commands(self):
        commands = []
        print(self.steps)
        print('-'*40)
        for container in self.steps:
            step = container["step"]
            commands.append(self.get_command(step))

        return commands

    def run(self):
        for command in self._commands():
            print('+ {}'.format(command))
            proc = subprocess.Popen(command.split())

            return_code = proc.wait()
            if return_code != 0:
                return return_code

        return 0

