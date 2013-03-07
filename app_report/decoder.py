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

import base64
import app_report


class Decoder(object):

    @staticmethod
    def decode_base64(encoded):
        return base64.b64decode(encoded)

    @classmethod
    def decode(cls, encoded, encoding='base64'):
        supported = ('base64', )

        if not encoded:
            raise app_report.errors.DecoderError("Encoded can't be blank!")

        elif not encoding:
            raise app_report.errors.DecoderError("Encoding can't be blank!")

        elif encoding not in supported:
            raise app_report.errors.DecoderError("Encoding '%s' not supported, only %s." % (encoding, supported))

        return getattr(cls, "decode_%s" % encoding)(encoded)
