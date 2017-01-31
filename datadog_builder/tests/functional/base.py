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

import os
import uuid

import betamax
import requests

from datadog_builder import client
from datadog_builder.tests import base
from datadog_builder.tests.functional import serializer


betamax.Betamax.register_serializer(serializer.YAMLSerializer)

DATADOG_API_KEY = os.environ.get('DATADOG_API_KEY', uuid.uuid4().hex)
DATADOG_APP_KEY = os.environ.get('DATADOG_APP_KEY', uuid.uuid4().hex)


with betamax.Betamax.configure() as config:
    config.define_cassette_placeholder('<DATADOG_API_KEY>', DATADOG_API_KEY)
    config.define_cassette_placeholder('<DATADOG_APP_KEY>', DATADOG_APP_KEY)

    config.cassette_library_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'cassettes')

    config.default_cassette_options['serialize_with'] = \
        serializer.YAMLSerializer.name


class TestCase(base.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()

        self.session = requests.Session()

        # setup api_key and app_key according to the betamax so it'll match
        self.client = client.DataDogClient.from_options(
            session=self.session,
            api_key=DATADOG_API_KEY,
            app_key=DATADOG_APP_KEY)

        self.recorder = betamax.Betamax(self.session)

        r = self.recorder.use_cassette(self.id())
        self.addCleanup(r.stop)
        r.start()
