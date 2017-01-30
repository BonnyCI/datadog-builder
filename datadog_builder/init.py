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

import datadog
import yaml

from datadog_builder import common
from datadog_builder import constants
from datadog_builder import schema


def add_arguments(subparsers):
    common.create_subcommand(subparsers,
                             'init',
                             init_command,
                             add_config=False,
                             help='Dump the current state of all monitors.')


def _render_monitor(monitor):
    keys = schema.monitor['properties'].keys()

    monitor = {k: v for k, v in monitor.items() if k in keys}

    tags = monitor.pop('tags', [])

    try:
        tags.remove(constants.TAG)
    except ValueError:
        pass

    if tags:
        monitor['tags'] = tags

    return monitor


def init_command(args):
    common.initialize(args)

    monitors = [_render_monitor(m) for m in datadog.api.Monitor.get_all()]

    output = {'monitors': monitors}

    print(yaml.dump(output, indent=2, default_flow_style=False))
