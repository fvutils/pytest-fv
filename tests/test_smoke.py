import os
import pytest
from pytest_fv import *
from .test_util import Util


@pytest.fixture
def setup(pytestconfig):
    print("setup: root=%s ini=%s" % (
        pytestconfig.rootdir,
        pytestconfig.inipath))
    return "setup"

@pytest.fixture
def design_source(fusesoc, setup):
    print("design_source")
#    dir = os.path.dirname(os.path.abspath(__file__))
#    fusesoc.add_library(dir)
#    files = fusesoc.getFiles("a:b:c")
#    print("files: %s" % str(files))
#    return files

@pytest.fixture
def sim_image(design_source, hdl_tool_sim, setup, request):
    print("design_source: %s" % design_source)
    print("test is: %s" % request.node.name)
    return hdl_tool_sim
    return "abc"

def test_smoke(request):
    util = Util(request)

    util.mkFile("top.sv", """
    module top;
        initial begin
            $display(">> Hello World");
            $finish;
        end
    endmodule
    """)

    util.mkCore("smoke", ["top.sv"])

    fs = FuseSoc()
    fs.add_library(util.test_rundir)

    files = fs.getFiles("smoke")
    print("files: %s" % str(files))

#    sim = HdlSim.create("ivl")
#    sim = HdlSim.create("xsm")
    sim = HdlSim.create("vl")

    build_args = sim.mkBuildArgs(util.test_rundir)
    build_args.addFiles(files)
    build_args.top.add("top")

    sim.build(build_args)

    run_args = sim.mkRunArgs(util.test_rundir, util.test_rundir)
    sim.run(run_args)

    util.assertLineExists(
        os.path.join(util.test_rundir, 'run.log'),
        ">> Hello World")



