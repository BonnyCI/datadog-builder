# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import argparse
import json
import logging
import logging.config
import os
import sys

import yaml

from datadog_builder import init
from datadog_builder import update
from datadog_builder import validate


LOG = logging.getLogger(__name__)


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()

    parser.add_argument('--config',
                        dest='auth_config',
                        # required=True,
                        type=argparse.FileType('r'),
                        help='Authentication Information')

    parser.add_argument('-l', '--logging',
                        dest='logging',
                        type=argparse.FileType('r'),
                        help='Logging configuration file')

    subparsers = parser.add_subparsers()

    init.add_arguments(subparsers)
    update.add_arguments(subparsers)
    validate.add_arguments(subparsers)

    args = parser.parse_args(argv)

    if args.logging:
        name, ext = os.path.splitext(args.logging.name)
        if ext in ('.yml', '.yaml'):
            logging_config = yaml.safe_load(args.logging)
        elif ext == '.json':
            logging_config = json.load(args.logging)
        else:
            m = "Don't know how to load file %s. Must be .json or .yaml"
            raise TypeError(m % args.logging.name)

        logging.config.dictConfig(logging_config)

    else:
        logging.basicConfig(level=logging.INFO)

    LOG.debug("Starting Up")
    args.func(args)


if __name__ == '__main__':
    main()
