import codecs
import os
import re

from setuptools import Command, setup

BASE_PATH = os.path.abspath(os.path.dirname(__file__))


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


def get_version():
    changes_path = os.path.join(BASE_PATH, "CHANGES.rst")
    regex = r"^#*\s*(?P<version>[0-9]+\.[0-9]+(\.[0-9]+)?)$"
    with codecs.open(changes_path, encoding="utf-8") as changes_file:
        for line in changes_file:
            res = re.match(regex, line)
            if res:
                return res.group("version")
    return "0.0.0"


version = get_version()


class VersionCommand(Command):
    description = "print current library version"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(version)


setup(
    name="pytest-deadfixtures",
    version=version,
    author="João Luiz Lorencetti",
    author_email="me@dirtycoder.net",
    maintainer="João Luiz Lorencetti",
    maintainer_email="me@dirtycoder.net",
    license="MIT",
    url="https://github.com/jllorencetti/pytest-deadfixtures",
    description="A simple plugin to list unused fixtures in pytest",
    long_description=read("README.rst"),
    py_modules=["pytest_deadfixtures"],
    install_requires=["pytest>=3.0.0"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    cmdclass={"version": VersionCommand},
    entry_points={"pytest11": ["deadfixtures = pytest_deadfixtures"]},
)
