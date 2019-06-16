"""
Author: xuxiongfeng
Date: 2019-06-13 17:05
Usage: 
"""
from collections import OrderedDict

from setuptools import setup, find_packages

setup(
    name="scrapy_pytest",
    version="0.1.0",
    keywords=("scrapy", "pytest", "unittest scrapy"),
    description="easy to test functions of scrapy spiders ",
    project_urls=OrderedDict(
        (
            ("Code", "https://github.com/Barnettxxf/scrapy_pytest"),
        )
    ),
    license="MIT",
    author="Barnett Xu",
    author_email="15102096586@163.com",
    packages=find_packages("src"),
    package_data={
        'scrapy_pytest': ['web/templates/*.html', 'web/static/*'],
    },
    package_dir={"": "src"},
    long_description="""Rapid create test cases file for scrapy spider""",
    platforms="any",
    install_requires=[
        "scrapy",
        "pytest",
        "flask",
        "flask_sqlalchemy",
        "flask_paginate",
    ],
    entry_points={
        "console_scripts": ["cacheweb = scrapy_pytest.server:cli"]}
)
