from xml_base import XmlBase
from gluon.html import TAG


class XmlWeb2py(XmlBase):

    @staticmethod
    def rows_to_xml(rows, fields, parent_tag, child_tag, response=None):
        return TAG[parent_tag](*[TAG[child_tag](*[TAG[field](row[field]) for field in fields]) for row in rows])
