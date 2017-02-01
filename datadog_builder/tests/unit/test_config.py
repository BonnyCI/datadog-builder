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

from datadog_builder import common
from datadog_builder.tests.unit import base


class ConfigTests(base.TestCase):

    def load_config(self, config_data):

        class _Args(object):
            def __init__(self, config):
                self.config = config

        return common.load_config(_Args(config_data))

    def test_override_defaults(self):
        config = self.load_config("""
          defaults:
            monitors:
               options:
                 new_host_delay: 300
                 no_data_timeframe: 2
               multi: false

          monitors:
            - name: a test monitor
              message: |
                I'm a test!
              multi: true
              options:
                notify_no_data: true
                new_host_delay: 400
              type: service check
              query: abc
        """)

        self.assertEqual({
            'monitors': [{'name': 'a test monitor',
                          'message': "I'm a test!\n",
                          'multi': True,
                          'options': {'notify_no_data': True,
                                      'new_host_delay': 400,
                                      'no_data_timeframe': 2},
                          'type': 'service check',
                          'query': 'abc'}]
        }, config)
