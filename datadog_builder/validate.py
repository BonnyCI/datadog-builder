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

import logging

from datadog_builder import common
from datadog_builder import client

from uuid import uuid4

LOG = logging.getLogger(__name__)

def add_arguments(subparsers):
    parser = common.create_subcommand(subparsers,
                                      'validate',
                                      validate_command,
                                      help='Validate config files')

    parser.add_argument('--round-trip',
                        action='store_true',
                        dest='round_trip',
                        help="Create/Delete test monitor for datadog validation")


def validate_command(args):
    config = common.load_config(args)

    if args.round_trip:
        c = client.DataDogClient.from_file(args.auth_config)

        for my_monitor in config.get('monitors', []):
            name = my_monitor['name']
            my_monitor['name'] = "{}-{}".format(uuid4(), name)

            my_monitor['id'] = _create_test_monitor(c, args, my_monitor)
            _delete_test_monitor(c, args, my_monitor)


def _create_test_monitor(client, args, monitor):
    LOG.info("Testing new monitor: %(name)s", monitor)
    try:
        return client.create_monitor(monitor)
    except HTTPError as exc:
        # Handle test failure here
        LOG.exception("Monitor %(name)s failed to create", monitor)
        LOG.error("Response body: %s", exc.response.text)


def _delete_test_monitor(client, args, monitor):
    LOG.info("Deleting test monitor: %(name)s", monitor)
    client.delete_monitor(monitor['id'])
