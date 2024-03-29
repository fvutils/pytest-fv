import os
import pytest

class DirConfig(object):

    def __init__(self, request : pytest.FixtureRequest):
        self.request = request
        self._rundir = os.path.join(os.getcwd(), "rundir")

    def builddir(self, name="build"):
        return os.path.join(self._rundir, name)
    
    def rundir(self, seed=None):
        print("module: %s" % str(self.request.module.__name__))
        return os.path.join(self._rundir, 
                            self.request.module.__name__ + "_" + self.request.node.name)
    
    def test_srcdir(self):
        return self.request.path


@pytest.fixture
def dirconfig(request):
    return DirConfig(request)
