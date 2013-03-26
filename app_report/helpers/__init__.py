# when running on web2py, try to import a specific module.

try:
    import gluon
    import jasper_web2py

    jasper_report = jasper_web2py.JasperWeb2py()
except ImportError:
    import jasper_base

    jasper_report = jasper_base.JasperBase()
