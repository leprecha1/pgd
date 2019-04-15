"""Setuptools script."""

from setuptools import setup, find_packages
from tfw_was import worker_class
from tfw_was import worker_class_helper

setup(
    name='pgd',
    version='1.0',
    description='Web Application - Google Dorks Crawler',
    long_description="Retrieve information by crawling Google Dorks.",
    classifiers=[
        "Programming Language :: Python"
    ],
    author='Rafael Lucas',
    author_email='rafael@flightpooling.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=worker_class.requires,
    extra_objects=["bin/headlessBrowser/geckodriver"]
)
