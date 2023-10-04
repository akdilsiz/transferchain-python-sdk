import unittest
from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


def test_suite():
    # crypt_test_loader = unittest.TestLoader()
    # crypt_test_suite = crypt_test_loader.discover(
    #    './transferchain/crypt/tests', pattern='test_*.py')
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    # test_suite.addTests(crypt_test_suite)
    return test_suite


setup(
    name="transferchain",
    version="v0.1.0",
    author="transferchain",
    description="transferchain python sdk",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TransferChain/transferchain-python-sdk",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
    test_suite='setup.test_suite'
)
