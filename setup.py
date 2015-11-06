from __future__ import with_statement
from setuptools import setup
from os.path import join


with open(join('src', 'basicstruct.py')) as f:
    for line in f:
        if line.startswith('__version__'):
            version = eval(line.split('=')[-1])


setup(
    name='basicstruct',
    version=version,
    description="A simple struct-like object for Python",
    long_description=open('README.rst').read(),
    license='MIT',
    author='Amir Rachum',
    author_email='amir@rachum.com',
    url='https://github.com/Nurdok/basicstruct/',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='struct, bean, basic struct, record, slots',
    package_dir={'': 'src'},
    py_modules=['basicstruct'],
    install_requires=['six'],
    test_require=['nose'],
    test_suite='nose.collector',
)
