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

import app_report.errors


class Configuration(object):

    keys = [
        'app_name',
        'access_key',
        'secret_key',
        'expires_signed_url_after',
    ]

    def __init__(self):
        # expire urls after 10 minutes, by default.
        self._expires_signed_url_after = 600

        for key in self.keys:
            if not hasattr(self, key):
                setattr(self, key, None)

    @property
    def expires_signed_url_after(self):
        return self._expires_signed_url_after

    @expires_signed_url_after.setter
    def expires_signed_url_after(self, value):
        if not isinstance(value, int) or value < 1:
            raise app_report.errors.InvalidConfigurationError("value must be an integer > 0, not %s" % value)

        self._expires_signed_url_after = value

    def validates(self):
        for key in self.keys:
            if not getattr(self, key):
                raise app_report.errors.RequiredConfigurationError("%s is required" % key)
