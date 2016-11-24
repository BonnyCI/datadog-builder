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

import jsonschema


common_options = {
    'type': 'object',
    'additionalProperties': True,
    'properties': {
        'silenced': {
            'type': 'object'
        },
        'notify_no_data': {
            'type': 'boolean'
        },
        'new_host_delay': {
            'type': 'integer',
        },
        'no_data_timeframe': {
            'type': 'integer',
        },
        'timeout_h': {
            'type': 'integer',
        },
        'require_full_window': {
            'type': 'boolean'
        },
        'renotify_interval': {
            'type': 'integer',
        },
        'escalation_message': {
            'type': 'string',
        },
        'notify_audit': {
            'type': 'boolean'
        },
        'locked': {
            'type': 'boolean'
        },
        'include_tags': {
            'type': 'boolean'
        },
    }
}


monitor = {
    'type': 'object',
    'additionalProperties': False,
    'required': ['name', 'message', 'type', 'query'],
    'properties': {
        'name': {
            'type': 'string',
        },
        'type': {
            'type': 'string',
            'enum': ['metric alert',
                     'service check',
                     'event alert'],
        },
        'message': {
            'type': 'string',
        },
        'query': {
            'type': 'string',
        },
        'options': common_options,
        'multi': {
            'type': 'boolean',
        },
        'tags': {
            'type': 'array',
            'items': {
                'type': 'string'
            }
        },
    },
}


schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'type': 'object',
    'additionalProperties': False,
    'required': ['monitors'],
    'properties': {
        'monitors': {
            'type': 'array',
            'items': monitor,
        }
    }
}


def validate(config):
    jsonschema.validate(config, schema)
