from __future__ import print_function

import argparse
import os
import sys

from wowlint.linter import Linter
from wowlint.validation.core import Severity


def plural(num):
    return "s" if num != 1 else ""


def wowlint(args, stream=sys.stdout):
    linter = Linter(Severity.ERROR if args.errors_only else None)

    longestFileName = 0

    highestSeverityEncountered = None

    countFiles = 0
    countFilesWithError = 0
    countErrors = 0
    countWarnings = 0

    for subject in args.file:
        if os.path.isfile(subject):
            countFiles += 1
            issues = linter.lint(subject)
            if len(issues) > 0:
                highestSeverityEncountered = max(max(map(lambda i: i.severity, issues), highestSeverityEncountered))
                longestFileName = max(longestFileName, len(subject))

                newErrors = len([i for i in issues if i.severity == Severity.ERROR])
                countErrors += newErrors
                if newErrors > 0:
                    countFilesWithError += 1
                countWarnings += len([i for i in issues if i.severity == Severity.WARNING])

                if args.list:
                    print(subject, file=stream)
                else:
                    for issue in issues:
                        print (
                            "{:{width}}: {:8} {}".format(
                                subject,
                                issue.severity,
                                issue.message,
                                width=longestFileName + 2
                            ),
                            file=stream
                        )

    if not (args.list or args.no_summary):
        if args.errors_only:
            print (
                "{} file{}, {} failed, {} error{}".format(
                    countFiles, plural(countFiles),
                    countFilesWithError,
                    countErrors, plural(countErrors)
                ),
                file=stream
            )
        else:
            print (
                "{} file{}, {} failed, {} error{}, {} warning{}".format(
                    countFiles, plural(countFiles),
                    countFilesWithError,
                    countErrors, plural(countErrors),
                    countWarnings, plural(countWarnings)
                ),
                file=stream
            )

    if highestSeverityEncountered >= Severity.ERROR:
        return 1


def getArgumentsParser():
    parser = argparse.ArgumentParser(description='Lint and validate Words of Worship resource files.')
    parser.add_argument('file', nargs='+', help='File(s) to validate')
    parser.add_argument('-e', '--errors-only', action='store_true', help='Only show errors, not warnings')
    parser.add_argument('-l', '--list', action='store_true', help='Only list files, not error details')
    parser.add_argument('-S', '--no-summary', action='store_true', help='Don\'t print summary at end (default when -l is given)')
    return parser


def main():
    args = getArgumentsParser().parse_args()
    retVal = wowlint(args, sys.stdout)
    sys.exit(retVal)


if __name__ == "__main__":
    main()
