import logging
import argparse

from api.api import LibcloudApi
from api.config import ApiConfiguration as configuration


def main(args):
    if args.debug is not None:
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)

    config = configuration()
    if config.is_certificate_validation_enabled():
        import libcloud.security
        libcloud.security.VERIFY_SSL_CERT = False

    api = LibcloudApi(config)
    api.build_controllers()
    api.start()

if '__main__' == __name__:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    main(args)
