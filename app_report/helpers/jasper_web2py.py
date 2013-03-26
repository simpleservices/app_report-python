from jasper_base import JasperBase


class JasperWeb2py(JasperBase):

    def __call__(self, response=None, content_disposition='attachment', **attributes):

        raw = JasperBase.__call__(self, **attributes)

        if response:
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = '%s; filename=%s.pdf' % (content_disposition, self.template_name)

        return raw
