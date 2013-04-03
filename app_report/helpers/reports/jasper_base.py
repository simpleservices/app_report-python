import app_report


class JasperBase(object):

    _default_attributes = {
        'data_type': 'xml',
        'args': {}
    }

    def __init__(self):
        self.attributes = {}

    def __call__(self, **attributes):

        self.attributes.update(attributes)

        for key in app_report.report.Jasper.attribute_keys:
            if key not in self.attributes:
                self.attributes[key] = self._default_attributes.get(key, None)

        # by default, xpath_expression is set to '/template_name(plural)/template_name(singular)'
        if not self.attributes['xpath_expression']:
            template_name = self.attributes['template_name']
            plural = template_name if template_name.endswith('s') else '%ss' % template_name
            singular = plural[:-1]

            self.attributes['xpath_expression'] = '/%s/%s' % (plural, singular)

        api = app_report.api.Jasper()
        report = app_report.report.Jasper(**self.attributes)

        return api.build(report)
