# Copyright 2012-2013 Isotoma Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

from twisted.internet import defer
from buildbot.process.buildstep import SUCCESS
from buildbot.steps import shell

from .base import ConfigurableStep
from ..travisyml import TRAVIS_HOOKS


class ShellCommand(shell.ShellCommand):

    flunkOnFailure = True
    haltOnFailure = True
    warnOnWarnings = True

    def setupEnvironment(self, cmd):
        """ Turn all build properties into environment variables """
        shell.ShellCommand.setupEnvironment(self, cmd)
        env = {}
        for k, v in self.build.getProperties().properties.items():
            env[str(k)] = str(v[0])
        if cmd.args['env'] is None:
            cmd.args['env'] = {}
        cmd.args['env'].update(env)

    def createSummary(self, stdio):
        self.updateStats(stdio)

    def setStatistics(self, key, value):
        pass

    def getStatistics(self, key, default):
        pass

    def updateStats(self, log):
        """
        Parse test results out of common test harnesses.

        Currently supported are:

         * Plone
         * Nose
         * Trial
         * Something mitchell wrote in Java
        """
        stdio = log.getText()

        total = passed = skipped = fails = warnings = errors = 0
        hastests = False

        # Plone? That has lines starting "Ran" and "Total". Total is missing if there is only a single layer.
        # For this reason, we total ourselves which lets us work even if someone runes 2 batches of plone tests
        # from a single target

        # Example::
        #     Ran 24 tests with 0 failures and 0 errors in 0.009 seconds

        if not hastests:
            outputs = re.findall(
                "Ran (?P<count>[\d]+) tests with (?P<fail>[\d]+) failures and (?P<error>[\d]+) errors", stdio)
            for output in outputs:
                total += int(output[0])
                fails += int(output[1])
                errors += int(output[2])
                hastests = True

        # Twisted

        # Example::
        #    FAILED (errors=5, successes=11)
        #    PASSED (successes=16)
        if not hastests:
            for line in stdio.split("\n"):
                if line.startswith("FAILED (") or line.startswith("PASSED ("):
                    hastests = True

                    line = line[8:][:-1]
                    stats = line.split(", ")
                    data = {}

                    for stat in stats:
                        k, v = stat.split("=")
                        data[k] = int(v)

                    if "successes" not in data:
                        total = 0
                        for number in re.findall("Ran (?P<count>[\d]+) tests in ", stdio):
                            total += int(number)
                        data["successes"] = total - sum(data.values())

        # This matches Nose and Django output

        # Example::
        #     Ran 424 tests in 152.927s
        #     FAILED (failures=1)
        #     FAILED (errors=3)

        if not hastests:
            fails += len(re.findall('FAIL:', stdio))
            errors += len(re.findall(
                '======================================================================\nERROR:', stdio))
            for number in re.findall("Ran (?P<count>[\d]+)", stdio):
                total += int(number)
                hastests = True

        # We work out passed at the end because most test runners dont tell us
        # and we can't distinguish between different test systems easily so we
        # might double count.
        passed = total - (skipped + fails + errors + warnings)

        # Update the step statistics with out shiny new totals
        if hastests:
            self.setStatistic('total', total)
            self.setStatistic('fails', fails)
            self.setStatistic('errors', errors)
            self.setStatistic('warnings', warnings)
            self.setStatistic('skipped', skipped)
            self.setStatistic('passed', passed)

    def describe(self, done=False):
        description = shell.ShellCommand.describe(self, done)

        if done and self.hasStatistic('total'):
            def append(stat, fmtstring):
                val = self.getStatistic(stat, 0)
                if val:
                    description.append(fmtstring % val)

            append("total", "%d tests")
            append("fails", "%d fails")
            append("errors", "%d errors")
            append("warnings", "%d warnings")
            append("skipped", "%d skipped")
            append("passed", "%d passed")

        return description


class TravisSetupSteps(ConfigurableStep):

    name = "setup-steps"
    haltOnFailure = True
    flunkOnFailure = True
    MAX_NAME_LENGTH = 50

    def addShellCommand(self, name, command):
        b = self.build

        step = ShellCommand(
            name=name,
            description=command,
            command=['/bin/bash', '-c', command],
        )

        step.setBuild(b)
        step.setWorker(b.workerforbuilder.worker)
        b.steps.append(step)

    def truncateName(self, name):
        name = name.lstrip("#")
        name = name.lstrip(" ")
        name = name.split("\n")[0]
        if len(name) > self.MAX_NAME_LENGTH:
            name = name[:self.MAX_NAME_LENGTH - 3] + "..."
        return name

    @defer.inlineCallbacks
    def run(self):
        config = yield self.getStepConfig()

        for k in TRAVIS_HOOKS:
            for command in getattr(config, k):
                self.addShellCommand(
                    name=self.truncateName(command),
                    command=command,
                )

        defer.returnValue(SUCCESS)
