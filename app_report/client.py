"""
This file is part of AppReport.

AppReport is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, version 3 of the License.

AppReport is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with AppReport.  If not, see <http://www.gnu.org/licenses/>.
"""

from urlparse import urljoin
import simplejson as json
import requests
import app_report


class Client(object):
    endpoint = 'http://reports.simpleservic.es'
    connection = requests

    @classmethod
    def build_url(cls, path):
        return urljoin(cls.endpoint, path)

    @classmethod
    def post(cls, path, params={}):
        url = cls.build_url(path)
        params = json.dumps(params)
        headers = {'content-type': 'application/json'}

        response = cls.connection.post(url, data=params, headers=headers)
        cls.raise_error_messages(response.json())

        return response

    @classmethod
    def raise_error_messages(cls, json_data):
        if 'messages' in json_data and json_data['messages'].get('has_any_error', False):
            messages = ' '.join({message.get('message', 's') for message in json_data.get('messages', []).get('messages', [])})
            raise app_report.errors.APIError('[%s]' % messages)
