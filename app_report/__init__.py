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

import errors
from configuration import Configuration
from client import Client
import report
import api
from signer import Signer
from decoder import Decoder
import helpers


class AppReport:
    settings = Configuration()

    @classmethod
    def configure(cls, config):
        for key, value in config.items():

            if key not in cls.settings.keys:
                raise errors.InvalidConfigurationKeyError("invalid configuration key: %s" % key)

            setattr(cls.settings, key, value)

        cls.settings.validates()
        return cls.settings
