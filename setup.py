from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


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
)
