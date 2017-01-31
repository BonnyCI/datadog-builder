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

import uuid

from datadog_builder import client
from datadog_builder.tests.unit import base


SYSTEM_LOAD = {
    'message': "{{#is_warning}} system load over 1.5 {{/is_warning}}\n",
    'multi': True,
    'name': 'system load on {{host.name}}',
    'options': {
        'locked': False,
        'new_host_delay': 300,
        'no_data_timeframe': 2,
        'notify_audit': False,
        'notify_no_data': False,
        'renotify_interval': 0,
        'require_full_window': True,
        'silenced': {},
        'thresholds': {
            'critical': 2.0,
            'warning': 1.7,
        },
        'timeout_h': 0,
    },
    'query': 'avg(last_5m):avg:system.load.1{*} by {host} > 2',
    'type': 'metric alert',
}


class ClientTests(base.TestCase):

    def test_sends_api_key(self):
        url = self._url('fake')
        text = uuid.uuid4().hex
        api_key = uuid.uuid4().hex
        self.requests_mock.get(url, text=text)

        c = client.DataDogClient()
        c.api_key = api_key
        resp = c.get('fake')

        self.assertTrue(self.requests_mock.called_once)
        self.assertEqual(text, resp.text)
        self.assertEqual({'api_key': [api_key]},
                         self.requests_mock.last_request.qs)

    def test_sends_app_key(self):
        url = self._url('fake')
        text = uuid.uuid4().hex
        app_key = uuid.uuid4().hex
        self.requests_mock.get(url, text=text)

        c = client.DataDogClient()
        c.application_key = app_key
        resp = c.get('fake')

        self.assertTrue(self.requests_mock.called_once)
        self.assertEqual(text, resp.text)
        self.assertEqual({'application_key': [app_key]},
                         self.requests_mock.last_request.qs)

    def test_sends_api_and_app_key(self):
        url = self._url('fake')
        text = uuid.uuid4().hex
        api_key = uuid.uuid4().hex
        app_key = uuid.uuid4().hex
        self.requests_mock.get(url, text=text)

        c = client.DataDogClient()
        c.api_key = api_key
        c.application_key = app_key

        resp = c.get('fake')

        self.assertTrue(self.requests_mock.called_once)
        self.assertEqual(text, resp.text)
        self.assertEqual({'api_key': [api_key], 'application_key': [app_key]},
                         self.requests_mock.last_request.qs)


class MonitorsTests(base.TestCase):

    def test_simple_init(self):
        self.requests_mock.get(self._url('monitors'),
                               json=[SYSTEM_LOAD],
                               headers={'Content-Type': 'application/json'})
