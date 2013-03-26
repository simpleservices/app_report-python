from setuptools import setup, find_packages

__version__ = '0.0.2'


def long_description():
    with open('README.md') as f:
        return f.read()


def requirements():
    with open('requirements.txt') as reqs:
        return [line for line in reqs.read().split('\n') if (line and not line.startswith('#'))]

setup(
    name='app_report',
    packages=find_packages(),
    version=__version__,
    description='Python client to AppReport API',
    long_description=long_description(),
    author="Lucas D'Avila",
    author_email='lucas@lucasdavi.la',
    url='https://github.com/simple_services/app_report-python',
    keywords=['pdf', 'report', 'jasper', 'api'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
        'Development Status :: 3 - Alpha'
    ],
    install_requires=requirements()
)
