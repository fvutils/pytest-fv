.. pytest-fv documentation master file, created by
   sphinx-quickstart on Tue Apr 16 19:37:21 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyTest-FV - PyTest for Functional Verification
==============================================

Pytest-FV is a pytest extension that provides features for simulating and
verifying models captured in a hardware description language.

Pytest-FV enables you to define your test suites using pytest. It simplifies
this task by:

* Enabling the use of FuseSoC .core files to capture file lists
* Enabling addition of custom and local filelists to compilation
* Providing in-built support for common simulators
    * AMD X-Sim
    * Cadence Xcelium
    * Open-Source Verilator
    * Siemens-EDA Questa
    * Synopsys VCS
* Enabling mixing of custom commands into the build/run flow

All of this within the existing pytest framework, which enables:

* Flexible capture of requirements in Python
* Easy addition of custom computation
* Existing configuration and front-end tools

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
