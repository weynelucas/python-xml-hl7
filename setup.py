from setuptools import setup, find_packages
from io import open


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


version = '1.3.0'
repository = 'https://github.com/weynelucas/python-xml-hl7'

setup(
  name = "python-xml-hl7",
  packages = find_packages(),
  version = version,
  description = "A library for parsing HL7 (version 2.x) messages in XML format into Python objects",
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = "Lucas Weyne",
  author_email = "weynelucas@gmail.com",
  url = repository,
  download_url = "%s/archive/%s.tar.gz" % (repository, version),
  keywords = "hl7 health level xml python-hl7 python-xml-hl7 ",
  classifiers=[ 
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: Healthcare Industry',
    'Natural Language :: English',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Topic :: Text Processing',
    'Topic :: Text Processing :: Markup :: XML',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
  ],
)