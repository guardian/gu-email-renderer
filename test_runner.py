#!/usr/bin/python
import optparse
import sys
import os
import unittest

USAGE = """%prog SDK_PATH
Run unit tests for App Engine apps.

SDK_PATH    Path to the SDK installation"""


def main(sdk_path, test_path):
    os.environ['RUNNING_UNIT_TESTS'] = '1'
    sys.path.insert(0, sdk_path)
    import dev_appserver
    dev_appserver.fix_sys_path()
    suite = unittest.loader.TestLoader().discover(test_path)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    parser = optparse.OptionParser(USAGE)
    options, args = parser.parse_args()
    if len(args) != 1:
        print 'Error: Exactly 1 arguments required.'
        parser.print_help()
        sys.exit(1)
    TEST_PATH = "tests"
    SDK_PATH = args[0]
    main(SDK_PATH, TEST_PATH)
