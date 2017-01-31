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
import platform

import requests
import yaml

from datadog_builder import version


class DataDogClient(object):

    API_HOST = 'https://app.datadoghq.com'
    API_VERSION = 'v1'

    USER_AGENT = 'datadog-builder/%s %s %s/%s' % (
        version.version_string,
        requests.utils.default_user_agent(),
        platform.python_implementation(),
        platform.python_version())

    def __init__(self, session=None, api_host=API_HOST):
        if not session:
            session = requests.Session()

        self.session = session
        self.api_host = api_host

    @property
    def api_key(self):
        return self.session.params.get('api_key')

    @api_key.setter
    def api_key(self, value):
        self.session.params['api_key'] = value

    @api_key.deleter
    def api_key(self, value):
        self.session.params.pop('api_key', None)

    @property
    def application_key(self):
        return self.session.params.get('application_key')

    @application_key.setter
    def application_key(self, value):
        self.session.params['application_key'] = value

    @application_key.deleter
    def application_key(self, value):
        self.session.params.pop('application_key', None)

    @property
    def verify(self):
        return self.session.verify

    @verify.setter
    def verify(self, value):
        self.session.verify = value

    @verify.deleter
    def verify(self):
        self.session.verify = None

    @classmethod
    def from_options(cls, session=None, **kwargs):
        app_key = kwargs.pop('application_key',
                             kwargs.pop('app_key',
                                        os.environ.get('DATADOG_APP_KEY')))
        api_key = kwargs.pop('api_key',
                             os.environ.get('DATADOG_API_KEY'))
        api_host = kwargs.pop('api_host',
                              os.environ.get('DATADOG_API_HOST',
                                             cls.API_HOST))

        if kwargs:
            extra_keys = ", ".join(kwargs.keys())
            raise TypeError("Unexpected Arguments: %s" % extra_keys)

        c = cls(session=session, api_host=api_host)

        if app_key:
            c.application_key = app_key
        if api_key:
            c.api_key = api_key

        return c

    @classmethod
    def from_file(cls, filename, session=None):
        auth_options = yaml.safe_load(filename)
        return cls.from_options(session=session, **auth_options)

    def request(self, method, path, **kwargs):
        url = "{api_host}/api/{api_version}/{path}".format(
            api_host=self.api_host,
            api_version=self.API_VERSION,
            path=path.lstrip('/'))

        headers = kwargs.setdefault('headers', {})
        headers.setdefault('Accept', 'application/json')
        headers.setdefault('User-Agent', self.USER_AGENT)

        response = self.session.request(method, url, **kwargs)

        response.raise_for_status()
        return response

    def get(self, path, **kwargs):
        return self.request('GET', path, **kwargs)

    def post(self, path, **kwargs):
        return self.request('POST', path, **kwargs)

    def put(self, path, **kwargs):
        return self.request('PUT', path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request('DELETE', path, **kwargs)

    def create_monitor(self, monitor, **kwargs):
        self.post('/monitor', json=monitor, **kwargs)

    def list_monitors(self, **kwargs):
        return self.get('/monitor', **kwargs).json()

    def update_monitor(self, monitor_id, changes, **kwargs):
        url = '/monitor/{}'.format(monitor_id)
        self.put(url, json=changes, **kwargs)

    def delete_monitor(self, monitor_id, **kwargs):
        self.delete('/monitor/{}'.format(monitor_id), **kwargs)
