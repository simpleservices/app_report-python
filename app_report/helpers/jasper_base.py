import app_report


class JasperBase(object):

    def __init__(self):
        self._default_attributes = {
            'data_type': 'xml',
            'args': {}
        }

    def __call__(self, **attributes):
        for key in app_report.report.Jasper.attribute_keys:
            setattr(self, key, attributes.get(key, self._default_attributes.get(key, None)))

        # by default, xpath_expression is set to '/template_name(plural)/template_name(singular)'
        if not self.xpath_expression:
            plural = self.template_name if self.template_name.endswith('s') else '%ss' % self.template_name
            singular = plural[:-1]
            self.xpath_expression = '/%s/%s' % (plural, singular)

        api = app_report.api.Jasper()
        report = app_report.report.Jasper(**self.__dict__)

        return api.build(report)
