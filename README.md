## app_report-python  
  
Python client to [AppReport API](http://reports.simpleservic.es/), the AppReport API allows you to generate pdf reports based on Jasper library in a really simple way. 

### installation  
```console
# add to requirements.txt
app_report

# and run the install command 
$ pip install -r requirements.txt
```

### use

* First, draw your jasper report using your prefered tool, like [i-report designer](http://community.jaspersoft.com/project/ireport-designer), a powerfull opensource tool to design reports.  

* After, upload the .jrxml file to [AppReport site](http://reports.simpleservic.es/), as a "report template". 

* And then, just connect your app to AppReport API using this gem:

  ```python
  import app_report  

  app_report.AppReport.configure({
      'app_name': 'app',
      'access_key': 'app-access-key',
      'secret_key': 'app-secret-key'
  })    

  xml_data_source = open('data_source.xml', 'r').read()

  # or, if you are using some web framework, you can render a view, eg:
  xml_data_source = your_framework_render_method('products/data_source.xml')

  report_options = {  
      'template_name': 'products',
      'data_type': 'xml',
      'data': xml_data_source,
      'xpath_expression': '/products/product',
      'args': { :key => 'value' }
  }

  api = app_report.api.Jasper()
  report = app_report.report.Jasper(**report_options)

  pdf_raw = api.build(report)
  open('report.pdf', 'w').write(report)
    
  ```  

<b>Just it!</b> AppReport is a really simple, no complex configurations or boring installations are required, just connect to AppReport API and start generating reports!  
  
## Contribute  
You can contribute sending pull requests, don't forget to write tests for your code and check the pep8 conventions :)

### testing
```console
$ python -m unittest discover -v
```  

### checking pep8 conventions
```console
$ pip install -r development-requirements.txt  
$ pep8 --first --show-source .  

# p.s. we are not using the "Maximum Line Length" of 79 chars for this lib.
```  