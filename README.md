## app_report-python  
  
app_report-python is a Python client to the [AppReport API](http://reports.simpleservic.es/), it allows you to generate pdf reports based on Jasper library in a really simple way. 

### Installation  

* For **Web2py framework** users, please read [Using the AppReport client on Web2py Apps](https://github.com/simpleservices/app_report-python/wiki/Using-the-AppReport-client-on-Web2py-Apps).

* For **Windows** users, please read [How to install pip on Windows](https://github.com/simpleservices/app_report-python/wiki/How-to-install-pip-on-Windows).

* Or, if you are using **Python on Linux**, follow this steps:

  ```console
  # create a file requirements.txt and add this line:
  app_report

  # after save it, run the install command:
  $ pip install -r requirements.txt
  ```

### Try it now

* This example assumes that you already drawn your report using some tool like [i-report designer](http://community.jaspersoft.com/project/ireport-designer) and uploaded the .jrxml file to the [AppReport site](http://reports.simpleservic.es/), as a "report template",  
    
  to make the things easy, we did it for you :) yay donuts to us.

  ```python
  import app_report
  from app_report.helpers import jasper_report
  from urllib2 import urlopen

  app_report.AppReport.configure({
      'app_name': 'shop',
      'access_key': 'udPONmbmD01MnxzMVgiL',
      'secret_key': 'ExINJLBR1I6Au6Hu0gQQoQmTMXAZuHk1Tkx3N19V'
  })

  xml_data = urlopen('http://reports.simpleservic.es/sample_resources/products.xml').read()
  report = jasper_report(template_name='products', data=xml_data)

  open('report.pdf', 'w').write(report)
    
  ```  

<b>Just it!</b> AppReport is a really simple, no more complex configurations or boring installations are required, just connect to AppReport API and start generating reports!  
  
## Contribute  
You can contribute sending pull requests, don't forget to write tests for your code and check the pep8 conventions :)

```console
$ pip install -r development-requirements.txt  

$ fab test

$ fab check_pep8
# p.s. the "Maximum Line Length" (of 79 chars) convention are being ignored.
```  