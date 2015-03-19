from setuptools import setup, find_packages
import sys, os

version = '0.2.0'

long_description = open('README.rst').read()

setup(
      name='python-cfonb',
      version=version,
      description="Pure Python lib to read/write CFONB files.",
      long_description=long_description,
      classifiers=[],
      keywords='cfonb bank statement parser',
      author='Florent Pigout',
      author_email='fpigout@anybox.fr',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      test_suite = "cfonb.tests.test_all.suite"
      )
