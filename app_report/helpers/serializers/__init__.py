# when running on web2py, try to import a specific module.

try:
    import gluon
    import xml_web2py

    rows_to_xml = xml_web2py.XmlWeb2py.rows_to_xml

except ImportError:
    import xml_base

    rows_to_xml = xml_base.XmlBase.rows_to_xml
