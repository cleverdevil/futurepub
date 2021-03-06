# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='futurepub',
    version='0.1.0',
    description='Micropub endpoint for scheduling future posts to other micropub endpoints.',
    author='Jonathan LaCour',
    author_email='jonathan@cleverdevil.org',
    install_requires=[
        "pecan",
        "zappa",
        "requests"
    ],
    test_suite='futurepub',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=['ez_setup'])
)
