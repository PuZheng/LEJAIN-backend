from distutils.core import setup
from setuptools import find_packages
from setuptools.command.test import test as TestCommand
import sys

PACKAGE = "genuine_ap"
NAME = "Genuine-AP"
DESCRIPTION = ""
AUTHOR = "xiechao"
AUTHOR_EMAIL = "xiechao06@gmail.com"
URL = ""
DOC = __import__(PACKAGE).__doc__


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name=NAME,
    long_description=DOC,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    entry_points={
        "distutils.commands": [
            "make_test_data=genuine_ap.tools.make_test_data:InitializeTestDB",
        ]
    }

)
