class XmlBase(object):

    @staticmethod
    def rows_to_xml():
        raise NotImplementedError("rows_to_xml must be overwritten in a child class!")
