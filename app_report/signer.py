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

import hmac
from hashlib import sha1
import base64


class Signer(object):

    @staticmethod
    def to_utf8(string):
        if isinstance(string, unicode):
            return string.encode('utf-8')

        return unicode(string, 'utf-8').encode('utf-8')

    @classmethod
    def sign(cls, secret_key, string):
        string = cls.to_utf8(string)
        signed = hmac.new(secret_key, string, sha1).digest()

        return base64.b64encode(signed)
