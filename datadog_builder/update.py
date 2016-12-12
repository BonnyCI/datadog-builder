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

import datadog

from datadog_builder import common
from datadog_builder import constants

LOG = logging.getLogger(__name__)


def add_arguments(subparsers):
    parser = common.create_subcommand(subparsers,
                                      'update',
                                      update_command,
                                      help='Update datadog monitors')

    parser.add_argument('-n', '--dry-run',
                        action='store_true',
                        dest='dry_run',
                        help="Don't perform commands just test")

    parser.add_argument('--no-delete',
                        action='store_false',
                        dest='delete',
                        help="Don't delete unknown monitors")


def update_command(args):
    common.initialize(args)
    config = common.load_config(args)

    up_monitors = datadog.api.Monitor.get_all(monitor_tags=[constants.TAG])
    up_monitors = {m['name'].strip(): m for m in up_monitors}

    for my_monitor in config.get('monitors', []):

        my_monitor = _cleanup_monitor(my_monitor)
        name = my_monitor['name']  # missing key will be caught by schema

        try:
            up_monitor = up_monitors.pop(name)
        except KeyError:
            _create_monitor(args, my_monitor)
        else:
            _update_monitor(args, up_monitor, my_monitor)

    # anything left at this point is upstream but not in our file
    if args.delete:
        for up_monitor in up_monitors.values():
            _delete_monitor(args, up_monitor)


def _cleanup_monitor(monitor):
    """Cleanups to help matching and pushing clean config"""
    for param in ('name', 'message', 'query'):
        try:
            monitor[param] = monitor[param].strip()
        except KeyError:
            pass

    return monitor


def _create_monitor(args, monitor):
    LOG.info("Creating new monitor: %(name)s", monitor)
    monitor.setdefault('tags', []).append(constants.TAG)

    if args.dry_run:
        LOG.warn("Create new monitor %(name)s", monitor)
    else:
        datadog.api.Monitor.create(**monitor)


def _update_monitor(args, up_monitor, my_monitor):
    changes = {}

    # handle tags
    up_tags = set(up_monitor.get('tags', []))
    my_tags = set(my_monitor.pop('tags', []) + [constants.TAG])

    if my_tags != up_tags:
        changes['tags'] = list(my_tags)

    # handle options
    up_options = up_monitor.get('options', {})
    my_options = my_monitor.pop('options', {})

    for k, v in my_options.items():
        if up_options.get(k) != v:
            changes.setdefault('options', {})[k] = v

    # handle the rest
    for k, v in my_monitor.items():
        if up_monitor[k] != v:
            changes[k] = v

    if changes:
        up_monitor['changed'] = ", ".join(changes.keys())
        LOG.info("Updating %(name)s because %(changed)s changed", up_monitor)

        if args.dry_run:
            LOG.warn("Updating monitor %(name)s from changed keys", up_monitor)
        else:
            datadog.api.Monitor.update(up_monitor['id'], **changes)

    else:
        LOG.debug("No changes to monitor %(name)s id: %(id)s", up_monitor)


def _delete_monitor(args, monitor):
    LOG.info("Deleting not found: %(name)s", monitor)

    if args.dry_run:
        LOG.warn('Deleting monitor %(id)s: %(name)s', monitor)
    else:
        datadog.api.Monitor.delete(monitor['id'])
