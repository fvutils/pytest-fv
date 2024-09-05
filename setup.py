
import os
import sys
from setuptools import setup, find_namespace_packages

version="0.0.1"

proj_dir = os.path.dirname(os.path.abspath(__file__))

try:
    sys.path.insert(0, os.path.join(proj_dir, "src/pytest_fv"))
    from __build_num__ import BUILD_NUM
    version += ".%s" % str(BUILD_NUM)
except ImportError as e:
    print("No build version: %s" % str(e))

    
setup(
  name = "pytest-fv",
  version = version,
  packages=find_namespace_packages(where='src'),
  package_dir = {'' : 'src'},
  author = "Matthew Ballance",
  author_email = "matt.ballance@gmail.com",
  description = "pytest extensions to support running functional-verification jobs",
  long_description="""
    PyTest extensions to support running functional-verification jobs
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
      'fusesoc',
      'pytest'
  ]
)

