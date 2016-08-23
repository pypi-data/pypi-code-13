import argparse
import sys
import os
import json
#sys.path.append(os.path.abspath('./../../'))
from throwie.Throwie import Throwie


def main():
    parser = argparse.ArgumentParser(description='Throwie - create/update tags on a collection of EC2 instances.')

    parser.add_argument('-f', '--filter_type', required=True,
        help='EC2 filter type, see EC2.Client.describe_instances for valid filter values')

    parser.add_argument('-i', '--inventory',
        help='EC2 filter values, space separated, could be private ip addresses or instance-id depending on filter type',
        required=True, nargs='+', type=str)

    parser.add_argument('-t', '--tags', required=True,
        help='EC2 tags in json format', type=json.loads)

    args = parser.parse_args()

    throwie = Throwie(args.filter_type, args.inventory)
    print throwie.tag_instances(args.tags)
