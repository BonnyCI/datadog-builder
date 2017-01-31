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

import os.path

import yaml

import betamax


class YAMLSerializer(betamax.BaseSerializer):

    name = 'datadog-yaml-serializer'

    @staticmethod
    def generate_cassette_name(cassette_library_dir, cassette_name):
        return os.path.join(cassette_library_dir,
                            '{0}.{1}'.format(cassette_name, 'yml'))

    def serialize(self, cassette_data):
        return yaml.safe_dump(cassette_data,
                              indent=2,
                              default_flow_style=False,
                              allow_unicode=True,
                              encoding='utf-8')

    def deserialize(self, cassette_data):
        try:
            deserialized_data = yaml.safe_load(cassette_data) or {}
        except yaml.YAMLError:
            deserialized_data = {}

        return deserialized_data
