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

from datadog_builder import client
from datadog_builder import common

from requests import HTTPError
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
                        help="Round-trip to datadog to validate monitors")


def validate_command(args):
    config = common.load_config(args)

    if args.round_trip:
        c = client.DataDogClient.from_file(args.auth_config)

        for monitor in config.get('monitors', []):
            monitor_name = monitor['name']
            monitor['name'] = "{}-{}".format(uuid4(), monitor_name)

            monitor_id = None
            try:
                LOG.debug("Creating test monitor: %(name)s", monitor)
                monitor_id = c.create_monitor(monitor)
            except HTTPError as exc:
                # Handle test failure here
                LOG.error("Monitor \"%s\" failed to round-trip validate",
                          monitor_name)
                LOG.error("Response body: %s", exc.response.text)
            else:
                LOG.info("Monitor \"%s\" round-trip validated successfully!",
                         monitor_name)
                LOG.debug("Deleting test monitor: %(name)s", monitor)
                c.delete_monitor(monitor_id)
