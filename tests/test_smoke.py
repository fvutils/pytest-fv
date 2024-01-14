import os
import pytest
from pytest_hdl import *
#import pytest_hdl


@pytest.fixture
def setup(pytestconfig):
    print("setup: root=%s ini=%s" % (
        pytestconfig.rootdir,
        pytestconfig.inipath))
    return "setup"

@pytest.fixture
def design_source(fusesoc, setup):
    print("design_source")
    dir = os.path.dirname(os.path.abspath(__file__))
    fusesoc.add_library(dir)
    files = fusesoc.getFiles("a:b:c")
    print("files: %s" % str(files))
    return files

@pytest.fixture
def sim_image(design_source, hdl_tool_sim, setup):
    print("design_source: %s" % design_source)
    return hdl_tool_sim
    return "abc"

def test_smoke(sim_image):
    print("test_smoke")
    print("design_source: %s" % str(design_source))