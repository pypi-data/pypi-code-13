# vi:et:ts=4 sw=4 sts=4
#
# local-pipelines : run Bitbucket pipelines locally
# Copyright (C) 2016  Gary Kramlich <grim@reaperworld.com>
# Copyright (C) 2016  Sean Farley <sean@farley.io>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

import fnmatch
import os
import subprocess

from pipelines.step import Step


class Pipeline(object):
    def __init__(self, config, path, branch, env=None):
        self.config = config
        self.build_path = os.path.abspath(path)
        self.branch = branch
        self.env = env or {}

        self.steps = self._get_steps()

    def _get_steps(self):
        if "branches" in self.config["pipelines"]:
            branches = self.config["pipelines"]["branches"]

            for pattern, steps in branches.iteritems():
                if fnmatch.fnmatch(self.branch, pattern):
                    return steps

        return self.config["pipelines"]["default"]

    def _determine_image(self, step):
        return step.image or self.config.get("image")

    def _get_command(self, step, script):
        workdir = "/opt/atlassian/bitbucketci/agent/build"

        labels = [
            "com.atlassian.pipelines.agent=\"local\"",
        ]

        volumes = [
            "{filename}:{filename}:ro".format(filename=script),
            "{path}:{workdir}:rw".format(
                path=self.build_path,
                workdir=workdir,
            ),
        ]

        cmd = [
            "docker",
            "run",
            "--rm=true",
            "--entrypoint=/bin/bash",
            "--memory=2048m",
            "-it",
            " ".join(["-v " + v for v in volumes]),
            "-w {}".format(workdir),
            " ".join(["--label " + l for l in labels]),
            " ".join(["-e " + k + "=" + v for k, v in self.env.iteritems()]),
            self._determine_image(step),
            script,
        ]

        return " ".join(cmd)

    def _steps(self):
        return [Step.from_dict(s["step"]) for s in self.steps]

    def run(self):
        return_code = 0

        for n, step in enumerate(self._steps()):
            script = step.script_file()
            command = self._get_command(step, script)

            try:
                print('+ {}'.format(command))
                proc = subprocess.Popen(command.split())

                return_code = proc.wait()
                if return_code != 0:
                    return return_code
            except KeyboardInterrupt:
                # let's not stacktrace on ctrl-c
                proc.kill()
                return_code = 1
                break
            finally:
                try:
                    os.remove(script)
                except OSError:
                    pass

        return return_code
