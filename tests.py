# coding=utf-8

import unittest

import simplejson as json
import requests
from httpretty import HTTPretty
from httpretty import httprettified
import os.path
from time import time
import base64

import app_report
from app_report import AppReport
from app_report.helpers import jasper_web2py
import test


class HelperTestCase(unittest.TestCase):

    fixture_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test', 'fixtures')

    @staticmethod
    def stub_post(path, params={}):
        uri = app_report.Client.build_url(path)
        params = json.dumps(params)

        HTTPretty.register_uri(method=HTTPretty.POST, uri=uri, body=params, content_type='text/json')

    @classmethod
    def fixture(cls, file_name):
        path = os.path.join(cls.fixture_path, file_name)
        return open(path, 'r')


class AppReportTestCase(HelperTestCase):

    def setUp(self):
        AppReport.configure({
            'app_name': 'app',
            'access_key': '123',
            'secret_key': '123abc'
        })

    def test_settings_is_instance_of_configuration(self):
        self.assertIsInstance(AppReport.settings, app_report.configuration.Configuration)

    def test_configure_return_settings(self):
        self.assertEqual(AppReport.configure({}), AppReport.settings)

    def test_configure_raise_invalid_configuration_key_error(self):
        with self.assertRaisesRegexp(app_report.errors.InvalidConfigurationKeyError, 'invalid configuration key: .*'):
            AppReport.configure({'invalid_key': 'foo'})

    def test_settings_validation(self):
        with self.assertRaisesRegexp(app_report.errors.RequiredConfigurationError, '.* is required'):
            AppReport.configure({'app_name': None})

    def test_configure_dict_change_settings(self):
        AppReport.configure({'app_name': 'app-name1'})

        self.assertEqual(AppReport.settings.app_name, 'app-name1')

    def test_settings_changed_via_atributes(self):
        AppReport.settings.app_name = 'app-name2'
        self.assertEqual(AppReport.settings.app_name, 'app-name2')


class ConfigurationTestCase(HelperTestCase):

    def setUp(self):
        self.default_settings = {
            'app_name': 'app',
            'access_key': '123',
            'secret_key': '123abc'
        }

        self.configuration = app_report.Configuration()

    def test_response_to_each_config_keys(self):
        for key in self.configuration.keys:
            self.assertTrue(hasattr(self.configuration, key), "Configuration must respond to %s" % key)

    def test_raises_required_configuration_error(self):
        for key in self.configuration.keys:
            if key == 'expires_signed_url_after':
                continue

            for k, v in self.default_settings.items():
                setattr(self.configuration, k, v)

            setattr(self.configuration, key, None)

            with self.assertRaisesRegexp(app_report.errors.RequiredConfigurationError, '.* is required'):
                self.configuration.validates()

    def test_expires_signed_url_after_validation(self):
        with self.assertRaisesRegexp(app_report.errors.InvalidConfigurationError, 'value must be an integer > 0, not .*'):
            self.configuration.expires_signed_url_after = None

        with self.assertRaisesRegexp(app_report.errors.InvalidConfigurationError, 'value must be an integer > 0, not .*'):
            self.configuration.expires_signed_url_after = 0

    def test_default_expires_signed_url_after_value(self):
        self.assertEqual(600, self.configuration.expires_signed_url_after)


class ClientTestCase(HelperTestCase):

    def test_default_endpoint(self):
        self.assertEqual('http://reports.simpleservic.es', app_report.Client.endpoint)

    def test_build_url(self):
        expected_url = 'http://reports.simpleservic.es/foo/bar'

        for path in ['/foo/bar', 'foo/bar']:
            given_url = app_report.Client.build_url(path)
            self.assertEqual(expected_url, given_url)

    def test_connection_is_requests(self):
        self.assertIs(app_report.Client.connection, requests)

    @httprettified
    def test_post_return_requests_response(self):
        path = '/requests_response.json'

        self.stub_post(path)
        response = app_report.Client.post(path)

        self.assertIsInstance(response, requests.models.Response)

    def test_raise_error_messages(self):
        expected_error_message = "\[This request requires a param 'access_key'. This request requires a param 'app_name'.\]"

        with self.assertRaisesRegexp(app_report.errors.APIError, expected_error_message):
            app_report.Client.raise_error_messages(json.load(self.fixture('error_messages.json')))

    @httprettified
    def test_post_raise_error_messages(self):
        path = 'error_messages.json'
        self.stub_post(path, json.load(self.fixture(path)))

        expected_error_message = "\[This request requires a param 'access_key'. This request requires a param 'app_name'.\]"

        with self.assertRaisesRegexp(app_report.errors.APIError, expected_error_message):
            app_report.Client.post(path)


class JasperReportTestCase(HelperTestCase):

    def setUp(self):
        self.default_attributes = {
            'template_name': 'my_super_template',
            'data_type': 'xml',
            'data': '<?xml version="1.0" encoding="utf-8"?><root><node></node></root>',
            'xpath_expression': '/root/node',
            'args': {'key': 'value'}
        }

        self.report_class = app_report.report.Jasper
        self.report = self.report_class(**self.default_attributes)

    def test_assignment_of_attributes(self):
        for key in self.report.attribute_keys:
            self.assertTrue(hasattr(self.report, key), 'report must respond to %s' % key)

    def test_response_to_validates_each_option(self):
        for key in self.report.attribute_keys:
            method = "validates_%s" % key
            self.assertTrue(hasattr(self.report, method), 'report must respond to %s' % method)

    def test_response_to_validates_all_attributes(self):
        self.assertTrue(hasattr(self.report, 'validates_all_attributes'), 'report must respond to validates_all_attributes')

    def test_response_to_alias_of_validates_all_attributes(self):
        self.assertTrue(hasattr(self.report, 'validates'), 'report must respond to validates')

    def test_response_to_validates_presence_of(self):
        self.assertTrue(hasattr(self.report, 'validates_presence_of'), 'report must respond to validates_presence_of')

    def test_validation_of_template_name(self):
        attributes = self.default_attributes.copy()
        attributes.pop('template_name')

        report = self.report_class(**attributes)

        for method in ('validates_template_name', 'validates_all_attributes', 'validates'):
            with self.assertRaisesRegexp(app_report.errors.ValidationError, 'template_name is required'):
                getattr(report, method)()

    # TODO test validation of other attributes in client side.


class SignerTestCase(HelperTestCase):

    def test_unicode_to_utf_8(self):
        expected = 'Some string é ê ç ê á ṕ ǵ ś'
        given = app_report.Signer.to_utf8(unicode(expected, 'utf-8'))

        self.assertEqual(expected, given)

    def test_str_to_utf_8(self):
        expected = 'Some string é ê ç ê á ṕ ǵ ś'
        given = app_report.Signer.to_utf8(expected)

        self.assertEqual(expected, given)

    def test_sign_strings(self):
        key = 'DrAGMrjPbJWHn+9ioJrA3s5/Q3ownDFBYZqFcZLm'
        string = 'Some string to sign => é ê ç ê á ṕ ǵ ś "a \'b <c/> \\d %e'

        expected_signature = 'k0YywdmJaMbQYfWXUZzRkc/Zhiw='
        given_signature = app_report.Signer.sign(secret_key=key, string=string)

        self.assertEqual(expected_signature, given_signature)


class BaseAPITestCase(HelperTestCase):

    def setUp(self):
        AppReport.configure({
            'app_name': 'app',
            'access_key': 'L3jC1SHoo3mqWZ2kT7m4',
            'secret_key': '6zD1sMPAYJdBj/SUMqi/BIqayWkjx3PSV1KaQyND'
        })

        self.base_api_class = app_report.api.Base
        self.base_api = self.base_api_class()

        # using fake api to test custom params

        self.fake_api = test.app_report.api.FakeAPI()

        self.fake_api.params = {
            'document': '123456789abc',
            'id': 123
        }

    def test_assignment_of_params(self):
        base_api = self.base_api_class()
        self.assertIsInstance(self.base_api.params, dict)

    def test_params_to_sign_return_an_empty_array(self):
        self.assertEqual([], self.base_api.params_to_sign())

    def test_sign_params_return_a_string(self):
        self.assertIsInstance(self.base_api.sign_params({}, []), str)

    def test_signed_params_is_a_hash(self):
        self.assertIsInstance(self.base_api.signed_params(), dict)

    def test_signed_params_include_configured_keys(self):
        signed_params = self.base_api.signed_params()

        for key in ('app_name', 'access_key'):
            self.assertTrue(key in signed_params, 'signed_params must include %s' % key)
            self.assertEqual(getattr(AppReport.settings, key), signed_params[key])

    def test_signed_params_include_expires(self):
        signed_params = self.base_api.signed_params()
        self.assertTrue('expires' in signed_params, 'signed_params must include expires')

    def test_configured_keys_not_overwritten_by_params(self):
        self.base_api.params['app_name'] = 'overwritten_app_name'
        self.base_api.params['access_key'] = 'overwritten_access_key'

        signed_params = self.base_api.signed_params()

        for key in ('app_name', 'access_key'):
            self.assertEqual(getattr(AppReport.settings, key), signed_params[key])

    def test_expires_not_overwritten_by_params(self):
        expires = 10
        self.base_api.params['expires'] = expires
        signed_params = self.base_api.signed_params()

        self.assertNotEqual(expires, signed_params['expires'])

    def test_signed_params_include_all_params_including_not_signed(self):
        self.fake_api.params['foo'] = 'new param value'
        signed_params = self.fake_api.signed_params()

        for key in self.fake_api.params:
            self.assertTrue(key in signed_params, 'signed_params must include %s' % key)

    def test_signed_params_include_expires(self):
        signed_params = self.base_api.signed_params()
        self.assertTrue('expires' in signed_params, 'signed_params must include expires')

    def test_signed_params_expires(self):
        expected = int(time()) + AppReport.settings.expires_signed_url_after
        calculated = self.base_api.signed_params()['expires']

        self.assertEqual(expected, calculated)

    def test_signed_params_include_signature(self):
        signed_params = self.base_api.signed_params()
        self.assertTrue('signature' in signed_params, 'signed_params must include signature')

    def test_sign_params_signature(self):
        params = {
            'foo': 'bar',
            'hey': "what's up?",
            'bar': 'foo',
        }

        ordered_keys = ('foo', 'hey', 'bar')
        params_string = ''.join(str(params[key]) for key in ordered_keys)

        expected_signature = app_report.Signer.sign(secret_key=AppReport.settings.secret_key, string=params_string)
        given_signature = self.base_api.sign_params(params, ordered_keys)

        self.assertEqual(expected_signature, given_signature)

    def test_signed_params_signature(self):
        # expected

        params = {}

        for param in self.fake_api.params_to_sign():
            params[param] = self.fake_api.params.get(param, '')

        params.update({
            'app_name': AppReport.settings.app_name,
            'expires': int(time()) + AppReport.settings.expires_signed_url_after
        })

        params_string = ''.join(str(params[key]) for key in self.fake_api.params_to_sign())

        expected_signature = app_report.Signer.sign(secret_key=AppReport.settings.secret_key, string=params_string)

        # given

        given_signature = self.fake_api.signed_params()['signature']

        self.assertEqual(expected_signature, given_signature)


class DecoderTestCase(HelperTestCase):

    def test_decode_base64(self):
        expected = 'Boring string...'
        encoded = base64.b64encode(expected)
        given = app_report.Decoder.decode_base64(encoded)

        self.assertEqual(expected, given)

    def test_decode_blank_encoded_error(self):
        for none_or_empty in (None, ''):
            with self.assertRaisesRegexp(app_report.errors.DecoderError, "Encoded can't be blank!"):
                app_report.Decoder.decode(none_or_empty)

    def test_decode_blank_encoding_error(self):
        for none_or_empty in (None, ''):
            with self.assertRaisesRegexp(app_report.errors.DecoderError, "Encoding can't be blank!"):
                app_report.Decoder.decode('encoded', none_or_empty)

    def test_decode_with_base64_encoding(self):
        expected = "Sexy string!"
        encoded = base64.b64encode(expected)
        given = app_report.Decoder.decode(encoded, 'base64')

        self.assertEqual(expected, given)

    def test_unsupported_encoding_error(self):
        encoding = 'unsuported-encoding'
        error_msg = "Encoding '%s' not supported, only .*" % encoding

        with self.assertRaisesRegexp(app_report.errors.DecoderError, error_msg):
            app_report.Decoder.decode('str', encoding)


class JasperAPITestCase(HelperTestCase):

    def setUp(self):

        AppReport.configure({
            'app_name': 'app-name',
            'access_key': 'access-key',
            'secret_key': 'secret-key'
        })

        self.default_report_options = {
            'template_name': 'some_report',
            'data_type': 'xml',
            'data': '<?xml version="1.0" encoding="utf-8"?><root><node></node></root>',
            'xpath_expression': '/root/node',
            'args': {'key': 'value'}
        }

        self.api = app_report.api.Jasper()
        self.report = app_report.report.Jasper(**self.default_report_options)

    def test_params_to_sign(self):
        params_to_sign = self.api.params_to_sign()

        for key in ('app_name', 'template_name', 'expires'):
            self.assertTrue(key in params_to_sign, 'params_to_sign must include %s' % key)

    # validation of report argument
    def test_validation_of_report_arg(self):
        for method in ('validates_report', 'build'):
            expected_error_msg = 'report must be a instance of app_report.report.Jasper not .*'

            with self.assertRaisesRegexp(app_report.errors.ValidationError, expected_error_msg):
                getattr(self.api, method)(None)

    # report validation, build! must call the validates! method of the report.
    def test_report_validation(self):
        report = app_report.report.Jasper()
        expected_error_msg = 'template_name is required'

        with self.assertRaisesRegexp(app_report.errors.ValidationError, expected_error_msg):
            self.api.build(report)

    def test_decode_blank_report_error(self):
        for none_or_empty in (None, ''):
            response_body = {'report': none_or_empty}

            with self.assertRaisesRegexp(app_report.errors.APIResponseError, "API returned a blank report!"):
                self.api.decode_report(response_body)

    def test_decode_report(self):
        expected = 'hello, am I a report?'

        response_body = {
            'report': {
                'encoding': 'base64',
                'encoded': base64.b64encode(expected)
            }
        }

        given = self.api.decode_report(response_body)
        self.assertEqual(expected, given)

    @httprettified
    def test_build_set_report_attributes_as_params(self):
        self.stub_post('/api/v1/factory/jasper/build.json', json.load(self.fixture('report.json')))

        self.api.build(self.report)

        for key in self.report.attribute_keys:
            self.assertTrue(key in self.api.params, 'params must include %s' % key)
            self.assertEqual(self.api.params[key], getattr(self.report, key))

    @httprettified
    def test_build(self):
        self.stub_post('/api/v1/factory/jasper/build.json', json.load(self.fixture('report.json')))

        expected_pdf_raw = self.fixture('report.pdf').read()
        given_pdf_raw = self.api.build(self.report)

        self.assertEqual(expected_pdf_raw, given_pdf_raw)


class JasperBaseHelperTestCase(HelperTestCase):

    def setUp(self):

        self.default_report_options = {
            'template_name': 'products',
            'data': '<?xml version="1.0" encoding="utf-8"?><root><node></node></root>'
        }

        self.helper = app_report.helpers.jasper_report

    def test_jasper_report_type(self):
        self.assertIsInstance(self.helper, app_report.helpers.jasper_base.JasperBase)

    @httprettified
    def test_default_attributes(self):
        self.stub_post('/api/v1/factory/jasper/build.json', json.load(self.fixture('report.json')))
        self.helper(**self.default_report_options)

        self.assertEqual('xml', self.helper.data_type)
        self.assertEqual({}, self.helper.args)

    @httprettified
    def test_default_xpath_expression(self):
        self.stub_post('/api/v1/factory/jasper/build.json', json.load(self.fixture('report.json')))
        self.helper(**self.default_report_options)

        self.assertEqual('/products/product', self.helper.xpath_expression)

    @httprettified
    def test_overwrite_default_attributes(self):
        self.stub_post('/api/v1/factory/jasper/build.json', json.load(self.fixture('report.json')))

        helper = app_report.helpers.jasper_report
        report_options = {
            'template_name': 'some_report',
            'data': '<?xml version="1.0" encoding="utf-8"?><root><node></node></root>',

            # default attributes
            'data_type': 'empty',
            'args': {'foo': 'bar'},
            'xpath_expression': '/root/node'
        }

        helper(**report_options)
        self.assertEqual('empty', helper.data_type)
        self.assertEqual({'foo': 'bar'}, helper.args)
        self.assertEqual('/root/node', helper.xpath_expression)

    @httprettified
    def test_assignment_of_attributes(self):
        self.stub_post('/api/v1/factory/jasper/build.json', json.load(self.fixture('report.json')))

        self.helper(**self.default_report_options)

        for key in self.default_report_options:
            self.assertTrue(hasattr(self.helper, key), 'helper must respond to %s' % key)
            self.assertEqual(getattr(self.helper, key), self.default_report_options[key])

    @httprettified
    def test_build(self):
        self.stub_post('/api/v1/factory/jasper/build.json', json.load(self.fixture('report.json')))

        expected_pdf_raw = self.fixture('report.pdf').read()
        given_pdf_raw = self.helper(**self.default_report_options)

        self.assertEqual(expected_pdf_raw, given_pdf_raw)


class JasperWeb2pyHelperTestCase(JasperBaseHelperTestCase):

    # inherits all tests from JasperBaseHelperTestCase

    def setUp(self):
        JasperBaseHelperTestCase.setUp(self)

        # overwrittes helper, because it tests will never run inside a web2py app
        self.helper = jasper_web2py.JasperWeb2py()

        self.fake_web2py_response = test.app_report.helpers.FakeWeb2pyResponse()

    def test_jasper_report_type(self):
        self.assertIsInstance(self.helper, app_report.helpers.jasper_web2py.JasperWeb2py)

    @httprettified
    def test_response_headers_change(self):
        self.stub_post('/api/v1/factory/jasper/build.json', json.load(self.fixture('report.json')))
        self.helper(response=self.fake_web2py_response, **self.default_report_options)

        expected_disposition = 'attachment; filename=%s.pdf' % (
            self.default_report_options['template_name']
        )

        self.assertEqual(self.fake_web2py_response.headers['Content-Type'], 'application/pdf')
        self.assertEqual(self.fake_web2py_response.headers['Content-Disposition'], expected_disposition)

    @httprettified
    def test_overwrite_content_disposition_(self):
        self.stub_post('/api/v1/factory/jasper/build.json', json.load(self.fixture('report.json')))
        self.helper(response=self.fake_web2py_response, content_disposition='foo', **self.default_report_options)

        expected_disposition = 'foo; filename=%s.pdf' % (
            self.default_report_options['template_name']
        )

        self.assertEqual(self.fake_web2py_response.headers['Content-Disposition'], expected_disposition)
