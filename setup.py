from setuptools import setup, find_packages
from io import open


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


version = '1.0.0'


setup(
  name = "python-xml-hl7",
  packages = find_packages(),
  version = version,
  description = "A library for parsing HL7 (version 2.x) messages in XML format into Python objects",
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = "Lucas Weyne",
  author_email = "weynelucas@gmail.com",
  url = "https://github.com/weynelucas/python-xml-hl7",
  download_url = "https://github.com/weynelucas/python-xml-hl7/archive/%s.tar.gz" % version,
  keywords = "hl7 xml python-hl7 python-xml-hl7",
  classifiers=[ 
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)