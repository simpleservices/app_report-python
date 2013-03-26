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


class Jasper(object):

    attribute_keys = (
        'template_name',
        'data_type',
        'data',
        'xpath_expression',
        'args'
    )

    def __init__(self, **attributes):
        for key in self.attribute_keys:
            setattr(self, key, attributes.get(key, None))

    # validation

    def validates_all_attributes(self):
        for key in self.attribute_keys:
            getattr(self, 'validates_%s' % key)()

    # alias
    validates = validates_all_attributes

    def validates_presence_of(self, attribute_name):
        if not getattr(self, attribute_name):
            raise app_report.errors.ValidationError("%s is required" % attribute_name)

    def validates_template_name(self):
        self.validates_presence_of('template_name')

    def validates_data_type(self):
        pass

    def validates_data(self):
        pass

    def validates_xpath_expression(self):
        pass

    def validates_args(self):
        pass
