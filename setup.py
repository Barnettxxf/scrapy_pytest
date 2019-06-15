"""
Author: xuxiongfeng
Date: 2019-06-13 17:05
Usage: 
"""
from collections import OrderedDict

from setuptools import setup, find_packages

# This is a list of files to install, and where
# (relative to the 'root' dir, where setup.py is)
# You could be more specific.

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
    # url="whatever",
    packages=find_packages("src"),
    package_dir={"": "src"},
    # scripts=["runner"],
    long_description="""Really long text here.""",
    platforms="any",
    install_requires=[
        "scrapy",
        "pytest"
    ],
)
