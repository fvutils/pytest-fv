import pytest

print("__ext__")

def pytest_addoption(parser : 'pytest.Parser'):
    parser.addoption(
        "--hdlsim-debug",
        action="store_true",
        dest="hdlsim_debug",
        help="[pytest-fv] Enables HDL simulator debug")
    parser.addoption(
        "--hdlsim",
        dest="hdlsim",
        help="[pytest-fv] Specifies the HDL simulator to use")

    parser.addini("hdlsim",
                help="[pytest-fv] Specifies the HDL simulator to use",
                type="string",
                default="vlt")

    parser.addini("libdirs",
                help="[pytest-fv] Specifies directories to search for FuseSoc files",
                type="pathlist",
                default="vlt")
