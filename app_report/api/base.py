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

from time import time
import app_report


class Base(object):

    def __init__(self):
        app_report.AppReport.settings.validates()
        self.params = {}

    def params_to_sign(self):
        return []

    def sign_params(self, params, ordered_keys):
        string = ''.join(str(params[key]) for key in ordered_keys)
        return app_report.Signer.sign(secret_key=app_report.AppReport.settings.secret_key, string=string)

    def signed_params(self):
        params = {}

        # include params that must be signed
        for param in self.params_to_sign():
            params[param] = self.params.get(param, '')

        # include configured keys
        params.update({
            'app_name': app_report.AppReport.settings.app_name,
            'expires': int(time()) + app_report.AppReport.settings.expires_signed_url_after,
        })

        # sign params
        params.update({
            'signature': self.sign_params(params, self.params_to_sign()),
            'access_key': app_report.AppReport.settings.access_key
        })

        # include not signed params
        _params = self.params.copy()
        _params.update(params)

        return _params
