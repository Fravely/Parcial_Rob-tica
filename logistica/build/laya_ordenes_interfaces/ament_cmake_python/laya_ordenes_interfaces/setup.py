from setuptools import find_packages
from setuptools import setup

setup(
    name='laya_ordenes_interfaces',
    version='0.1.0',
    packages=find_packages(
        include=('laya_ordenes_interfaces', 'laya_ordenes_interfaces.*')),
)
