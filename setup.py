from setuptools import setup, find_packages
import sys

from aave_python import __version__

if sys.version_info < (3, 9):
    sys.exit('Python 3.9+ required to install this package. Install it here: https://www.python.org/downloads/')


def readme():
    with open("README.md") as infile:
        return infile.read().strip()


setup(
    name='aave_python',
    version=__version__,
    author='Harrison Schick',
    author_email='hschickdevs@gmail.com',
    description='An unofficial Python3.9+ package that wraps Aave staking smart contracts',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='https://github.com/PathX-Projects/Aave-DeFi-Client',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[line.strip() for line in open('requirements.txt').readlines()],
)