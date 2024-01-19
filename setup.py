
import os, stat
from setuptools import setup, find_namespace_packages

version="0.0.1"

if "BUILD_NUM" in os.environ.keys():
    version += "." + os.environ["BUILD_NUM"]

setup(
  name = "pytest-fv",
  version = version,
  packages=find_namespace_packages(where='src'),
  package_dir = {'' : 'src'},
#  package_data = {'ivpm': ['scripts/*', 'templates/*', 'share/*', 'share/cmake/*']},
  author = "Matthew Ballance",
  author_email = "matt.ballance@gmail.com",
  description = (""),
  long_description="""
  """,
  license = "Apache 2.0",
  keywords = ["SystemVerilog", "Verilog", "RTL", "Coverage"],
  url = "https://github.com/fvutils/pytest-fv",
  # entry_points={
  #   'console_scripts': [
  #     'ivpm = ivpm.__main__:main'
  #   ]
  # },
  setup_requires=[
    'setuptools_scm',
  ],
  install_requires=[
      'fusesoc'
  ]
)

