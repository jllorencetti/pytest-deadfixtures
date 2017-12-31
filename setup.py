import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-deadfixtures',
    version='0.1.0',
    author='João Luiz Lorencetti',
    author_email='me@dirtycoder.net',
    maintainer='João Luiz Lorencetti',
    maintainer_email='me@dirtycoder.net',
    license='MIT',
    url='https://github.com/dirtycoder/pytest-deadfixtures',
    description='A simple plugin to list unused fixtures in pytest',
    long_description=read('README.rst'),
    py_modules=['pytest_deadfixtures'],
    install_requires=['pytest>=3.1.1'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'deadfixtures = pytest_deadfixtures',
        ],
    },
)
