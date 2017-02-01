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
import copy

import yaml

from datadog_builder import schema


def _recursive_merge(a, b, path=None):
    "merges b into a"
    if path is None:
        path = []

    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                _recursive_merge(a[key], b[key], path + [str(key)])
            elif isinstance(a[key], dict) or isinstance(b[key], dict):
                raise Exception("Can't merge dictionary and not dictionary")
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]

    return a


def load_config(args):
    job_config = yaml.safe_load(args.config)
    defaults = job_config.get('defaults', {})
    output = {}

    for job_type in ('monitors',):
        for job in job_config.get(job_type, []):
            job_output = copy.deepcopy(defaults.get(job_type, {}))
            _recursive_merge(job_output, copy.deepcopy(job))

            output.setdefault(job_type, []).append(job_output)

    schema.validate(output)
    return output


def create_subcommand(subparsers, command, func, add_config=True, **kwargs):
    parser = subparsers.add_parser(command, **kwargs)
    parser.set_defaults(func=func)

    if add_config:
        parser.add_argument('config',
                            type=argparse.FileType('r'),
                            help='Job information')

    return parser
