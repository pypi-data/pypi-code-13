from unittest.main import USAGE_AS_MAIN

from python_agent.test_listener.integrations import SealightsTestProgram

__unittest = True


def main():
    m = SealightsTestProgram
    SealightsTestProgram.USAGE = USAGE_AS_MAIN
    m(module=None)


if __name__ == '__main__':
    main()
