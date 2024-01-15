# pytest-fv
Support library for capturing functional verification test suites via Python unit tests

Pytest provides a useful framework of test fixtures to initialize infrastructure
required by a test. This project aspires to use that approach to incrementally 
define and setup the simulation and other functional-verification tools required
for a test to run. 

As a first phase, this project will provide a series of utility classes that help
to abstract common pieces of verification infrastructure -- for example, HDL 
simulators, from which users wish choose one of several.

Pytest-FV strongly encourages the use of FuseSoC to capture files in a modular
fashion, and provides utility classes for querying the FuseSoC database.


