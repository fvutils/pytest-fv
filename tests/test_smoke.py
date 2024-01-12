import os
import pytest
import pytest_hdl
from pytest_hdl import hdl_tool_sim, fusesoc

@pytest.fixture
def setup():
    print("setup")
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