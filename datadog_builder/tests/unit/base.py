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

import fixtures
import requests_mock
from requests_mock.contrib import fixture as requests_mock_fixture
import testtools

from datadog_builder import client

# requests-mock bug #1584008: do all matching as case sensitive
requests_mock.mock.case_sensitive = True


class TestCase(testtools.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()

        self.logger = self.useFixture(fixtures.FakeLogger(level=logging.DEBUG))
        self.requests_mock = self.useFixture(requests_mock_fixture.Fixture())

    @staticmethod
    def _url(*args):
        return "/".join([client.DataDogClient.API_HOST, 'api/v1'] +
                        [a.strip('/') for a in args])
