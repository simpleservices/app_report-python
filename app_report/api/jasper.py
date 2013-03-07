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

import app_report
from app_report.api import Base
import simplejson as json


class Jasper(Base):

    @staticmethod
    def params_to_sign():
        return ('app_name', 'template_name', 'expires')

    @staticmethod
    def validates_report(report):

        if not isinstance(report, app_report.report.Jasper):
            error_msg = "report must be a instance of app_report.report.Jasper not %s" % type(report)
            raise app_report.errors.ValidationError(error_msg)

    def build(self, report):
        self.report = report
        self.validates_report(self.report)
        self.report.validates()

        for key in self.report.attribute_keys:
            self.params[key] = getattr(self.report, key)

        path = '/api/v1/factory/jasper/build.json'
        response = app_report.Client.post(path, self.signed_params())

        return self.decode_report(response.json())

    @staticmethod
    def decode_report(response_body):
        report = response_body.get('report', '')

        if not report:
            raise app_report.errors.APIResponseError("API returned a blank report!")

        return app_report.Decoder.decode(report.get('encoded', ''), report.get('encoding', ''))
