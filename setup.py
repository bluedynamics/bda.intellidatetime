from setuptools import find_packages
from setuptools import setup
import os


def read_file(name):
    with open(os.path.join(os.path.dirname(__file__), name)) as f:
        return f.read()


version = '1.5.dev0'
shortdesc = 'bda.intellidatetime'
longdesc = '\n\n'.join([read_file(name) for name in [
    'README.rst',
    'LICENSE.rst'
]])


setup(
    name='bda.intellidatetime',
    version=version,
    description=shortdesc,
    long_description=longdesc,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
    keywords='',
    author='BlueDynamics Alliance',
    author_email='dev@bluedynamics.com',
    url=u'https://github.com/bluedynamics/bda.intellidatetime',
    license='Simplified BSD',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['bda'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zope.interface',
    ],
    test_suite='bda.intellidatetime.tests'
)
